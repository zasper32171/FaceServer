import pickle
import cv2
import numpy as np
import dlib

import resources.dlib

from .        import Handler
from .formats import Box, Boxes, BoxesInOutMixin


class DlibAlignRecognizeHandler(BoxesInOutMixin, Handler):

    _param_map = {'predictor':  (str,   'shape_predictor_5_face_landmarks.dat',      resources.dlib.PREDICTOR_LIST),
                  'model':      (str,   'dlib_face_recognition_resnet_model_v1.dat', resources.dlib.MODEL_LIST),
                  'classifier': (str,   'dlib_choke_g1.encodings',                   resources.dlib.CLASSIFIER_LIST),
                  'dim':        (int,   96, None),
                  'jitters':    (int,   1,   None),
                  'tresh':      (float, 0.6, None)}

    _keep_position = True

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._aligner = None
        self._encoder = None
        self._encodings = None

    def prepare(self):

        self._aligner = dlib.shape_predictor(
            resources.dlib.PREDICTOR_PATH + self._predictor
        )

        self._encoder = dlib.face_recognition_model_v1(
            resources.dlib.MODEL_PATH + self._model
        )

        with open(resources.dlib.CLASSIFIER_PATH + self._classifier, 'rb') as f:
            self._encodings = pickle.load(f)

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (self._dim, self._dim))

        rect = dlib.rectangle(0, 0, self._dim, self._dim)
        landmarks = self._aligner(rgb, rect)

        rep = self._encoder.compute_face_descriptor(
            rgb, landmarks, self._jitters
        )
        rep = np.array(rep)

        candidates = []

        for name, encoding in self._encodings:

            distance = np.linalg.norm(encoding - rep)
            candidates.append((name, distance))

        candidates = sorted(candidates, key=lambda candidate: candidate[1])

        name, distance = candidates[0]

        return Boxes([Box(label=name, prob=distance)])

    def finish(self):

        pass
