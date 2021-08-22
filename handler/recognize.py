import pickle
import cv2
import numpy as np

import openface
import facenet

from .        import Handler
from .formats import Box, Boxes, BoxesInOutMixin


class FacenetRecognizeHandler(BoxesInOutMixin, Handler):

    _param_map = {'model':           (str,    '20180402',              facenet.FACENET_MODEL_LIST),
                  'classifier':      (str,    '20180402_choke_g1.pkl', facenet.CLASSIFIER_LIST),
                  'dim':             (int,                 160,        None),
                  'gpu_memory_frac': ((float, type(None)), None,       None),
                  'tresh':           (float,               0.5,        None)}

    _keep_position = True

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self.encoder = None
        self.identifier = None

    def prepare(self):

        self.encoder = facenet.Encoder(
            facenet.FACENET_MODEL_PATH + self._model,
            self._gpu_memory_frac
        )

        self.identifier = facenet.Identifier(
            facenet.CLASSIFIER_PATH + self._classifier
        )

        self.execute_one(np.zeros((self._dim, self._dim, 3), dtype='uint8'))

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(frame, (self._dim, self._dim))

        rep = self.encoder.generate_embedding(rgb)

        name, prob = self.identifier.identify(rep)

        return Boxes([Box(label=name, prob=prob)])

    def finish(self):

        pass


class OpenfaceRecognizeHandler(BoxesInOutMixin, Handler):

    _param_map = {'model':      (str,   'nn4.small2.v1.t7',     openface.MODEL_LIST),
                  'classifier': (str,   'nn4.small2.v1.g1.pkl', openface.CLASSIFIER_LIST),
                  'dim':        (int,   96,                     None),
                  'gpu':        (bool,  True,                   None),
                  'tresh':      (float, 0.5,                    None)}

    _keep_position = True

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._net = None
        self._le  = None
        self._clf = None

    def prepare(self):

        self._net = openface.TorchNeuralNet(
            openface.MODEL_PATH + self._model, self._dim, self._gpu
        )

        with open(openface.CLASSIFIER_PATH + self._classifier, 'rb') as f:
            self._le, self._clf = pickle.load(f, encoding='latin1')

        self.execute_one(np.zeros((self._dim, self._dim, 3), dtype='uint8'))

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (self._dim, self._dim))

        rep = self._net.forward(rgb).reshape(1, -1)

        predictions = self._clf.predict_proba(rep).ravel()
        max_index = np.argmax(predictions)

        person = self._le.inverse_transform(max_index)
        confidence = predictions[max_index]

        return Boxes([Box(label=person, prob=confidence)])

    def finish(self):

        pass
