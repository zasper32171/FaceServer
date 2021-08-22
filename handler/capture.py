import time
import cv2

from . import Handler


class CaptureHandler(Handler):

    _param_map = {'source': ((int, str), 0,   None),
                  'width':  (int,        640, None),
                  'height': (int,        480, None),
                  'fps':    (int,        25,  None)}

    _num_input, _num_output = 0, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._capture = None

    def prepare(self):

        # '%d.jpg'
        self._capture = cv2.VideoCapture(self._source)

        if not self._capture.isOpened():
            exit(1)

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
        self._capture.set(cv2.CAP_PROP_FPS, self._fps)

    def execute(self):

        start = time.time()

        ret, frame = self._capture.read()

        # TODO: handle service end
        if not ret: exit(0)

        elapse = time.time() - start

        if elapse < 1 / self._fps:
            time.sleep(1 / self._fps - elapse)

        return frame

    def finish(self):

        self._capture.release()
