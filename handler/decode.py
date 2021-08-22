import cv2

from . import Handler


class DecodeHandler(Handler):

    _num_input, _num_output = 1, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def prepare(self):

        pass

    def execute(self, packet):

        frame = cv2.imdecode(packet, cv2.IMREAD_COLOR)

        return frame

    def finish(self):

        pass
