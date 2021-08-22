import cv2

from . import Handler


class RenderHandler(Handler):

    _param_map = {'fps': (int, 0, None)}

    _num_input, _num_output = 1, 0

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def prepare(self):

        pass

    def execute(self, frame):

        cv2.imshow('FaceClient', frame)

        if not self._fps == 0:
            cv2.waitKey(round(1 / self._fps * 1000))
        else:
            cv2.waitKey(1)

    def finish(self):

        cv2.destroyAllWindows()
