import cv2
import dlib

import resources.dlib

from .        import Handler
from .formats import Box, Boxes, BoxesInOutMixin


class HaarDetectFaceHandler(BoxesInOutMixin, Handler):

    _param_map = {'scale_factor': (float, 1.1, None),
                  'min_size':     (int,   20,  None)}

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._detector = None

    def prepare(self):

        self._detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        boxes = Boxes()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        result = self._detector.detectMultiScale(
            gray, scaleFactor=self._scale_factor,
            minSize=(self._min_size, self._min_size)
        )

        for (x, y, w, h) in result:

            crop = frame[y: y + h, x: x + w]

            frame_h, frame_w, _ = frame.shape

            x = min(max(x, 0), frame_w)
            y = min(max(y, 0), frame_h)
            w = min(max(w, 0), frame_w - x)
            h = min(max(h, 0), frame_h - y)

            boxes.append(Box('face', None, x, y, w, h, crop))

        return boxes

    def finish(self):

        pass


class HogDetectFaceHandler(BoxesInOutMixin, Handler):

    _param_map = {'upsample': (int, 1, None)}

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._detector = None

    def prepare(self):

        self._detector = dlib.get_frontal_face_detector()

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            result = self._detector(rgb, self._upsample)

        except Exception as e:
            print('Warning: %s: %s' % (type(e).__name__, e))
            result = []

        boxes = Boxes()

        for rect in result:

            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()

            frame_h, frame_w, _ = frame.shape

            x = min(max(x, 0), frame_w)
            y = min(max(y, 0), frame_h)
            w = min(max(w, 0), frame_w - x)
            h = min(max(h, 0), frame_h - y)

            crop = frame[y: y + h, x: x + w]

            boxes.append(Box('face', None, x, y, w, h, crop))

        return boxes

    def finish(self):

        pass


class MmodDetectFaceHandler(BoxesInOutMixin, Handler):

    _param_map = {'model':    (str,   'mmod_face_detector.dat', resources.dlib.DETECTOR_LIST),
                  'upsample': (int,   1,                        None),
                  'tresh':    (float, 0.5,                      None)}

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._detector = None

    def prepare(self):

        self._detector = dlib.cnn_face_detection_model_v1(
            resources.dlib.DETECTOR_PATH + self._model
        )

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            result = self._detector(rgb, self._upsample)

        except Exception as e:
            print('Warning: %s: %s' % (type(e).__name__, e))
            result = []

        boxes = Boxes()

        for rect in result:

            if rect.confidence < self._tresh:
                continue

            rect = rect.rect

            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()

            frame_h, frame_w, _ = frame.shape

            x = min(max(x, 0), frame_w)
            y = min(max(y, 0), frame_h)
            w = min(max(w, 0), frame_w - x)
            h = min(max(h, 0), frame_h - y)

            crop = frame[y: y + h, x: x + w]

            boxes.append(Box('face', None, x, y, w, h, crop))

        return boxes

    def finish(self):

        pass
