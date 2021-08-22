import cv2

from .        import Handler
from .formats import Frame, Boxes


class DrawBoxesHandler(Handler):

    _num_input, _num_output = 2, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def prepare(self):

        pass

    def execute(self, frame, boxes):

        assert isinstance(frame, Frame)
        assert isinstance(boxes, Boxes)

        for box in boxes:
            x, y, w, h = box.x, box.y, box.w, box.h
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        return frame

    def finish(self):

        pass


class DrawLabeledBoxesHandler(Handler):

    _num_input, _num_output = 2, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def prepare(self):

        pass

    def execute(self, frame, boxes):

        assert isinstance(frame, Frame)
        assert isinstance(boxes, Boxes)

        for box in boxes:

            x, y, w, h = box.x, box.y, box.w, box.h

            cv2.rectangle(
                frame, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=2
            )

            if box.label is None: continue

            (text_w, text_h), _ = cv2.getTextSize(
                box.label, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2
            )

            cv2.rectangle(
                frame, (x, y), (x + text_w, y - text_h), color=(255, 0, 255),
                thickness=cv2.FILLED
            )

            cv2.putText(
                frame, box.label, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=(0, 0, 0), thickness=2, lineType=1
            )

        return frame

    def finish(self):

        pass
