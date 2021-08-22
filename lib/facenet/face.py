import pickle
import os

import cv2
import numpy as np
import tensorflow as tf

from . import detect_face
from . import facenet


class Identifier:
    def __init__(self, model):
        with open(model, 'rb') as infile:
            self.model, self.class_names = pickle.load(infile)

    def identify(self, embedding):
        if embedding is not None:
            predictions = self.model.predict_proba([embedding])
            best_class_indices = np.argmax(predictions, axis=1)
            best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
            return self.class_names[best_class_indices[0]], best_class_probabilities[0]


class Encoder:
    def __init__(self, model, gpu_memory_fraction=None):
        if gpu_memory_fraction is not None:
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
        else:
            gpu_options = tf.GPUOptions(allow_growth=True)
        self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with self.sess.as_default():
            facenet.load_model(model)

    def generate_embedding(self, face):
        # Get input and output tensors
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        prewhiten_face = facenet.prewhiten(face)

        # Run forward pass to calculate embeddings
        feed_dict = {images_placeholder: [prewhiten_face], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]


class Detection:
    # face detection parameters
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    def __init__(self, model, face_crop_size=160, face_crop_margin=32, gpu_memory_fraction=None):
        self.pnet, self.rnet, self.onet = self._setup_mtcnn(model, gpu_memory_fraction)
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def _setup_mtcnn(self, model, gpu_memory_fraction):
        with tf.Graph().as_default():
            if gpu_memory_fraction is not None:
                gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            else:
                gpu_options = tf.GPUOptions(allow_growth=True)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                return detect_face.create_mtcnn(sess, model)

    def find_faces(self, image):
        faces = []

        bounding_boxes, _ = detect_face.detect_face(image, self.minsize,
                                                    self.pnet, self.rnet, self.onet,
                                                    self.threshold, self.factor)
        for bb in bounding_boxes:
            image_h, image_w, _ = image.shape
            
            x1 = int(round(np.maximum(bb[0] - self.face_crop_margin / 2, 0)))
            y1 = int(round(np.maximum(bb[1] - self.face_crop_margin / 2, 0)))
            x2 = int(round(np.minimum(bb[2] + self.face_crop_margin / 2, image_w)))
            y2 = int(round(np.minimum(bb[3] + self.face_crop_margin / 2, image_h)))

            cropped = image[y1: y2, x1: x2]
            resized = cv2.resize(cropped, (self.face_crop_size, self.face_crop_size), interpolation=cv2.INTER_LINEAR)

            faces.append(((x1, y1, x2, y2), resized))

        return faces
