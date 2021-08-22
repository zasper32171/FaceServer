import cv2

from . import Handler


class ResizeHandler(Handler):

    _param_map = {'width':  (int, 640, None),
                  'height': (int, 480, None)}

    _num_input, _num_output = 1, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def prepare(self):

        pass

    def execute(self, frame):

        resized = cv2.resize(frame, (self._width, self._height))

        return resized

    def finish(self):

        pass
