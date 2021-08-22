import cv2

from . import Handler


class EncodeHandler(Handler):

    _param_map = {'quality': (int, 80, None)}

    _num_input, _num_output = 1, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def prepare(self):

        pass

    def execute(self, frame):

        _, packet = cv2.imencode(
            '.jpg', frame,
            (cv2.IMWRITE_JPEG_QUALITY, self._quality)
        )

        return packet

    def finish(self):

        pass
