import numpy as np
import cv2

import facenet

from .        import Handler
from .formats import Box, Boxes, BoxesInOutMixin


class MtcnnDetectFaceAlignHandler(BoxesInOutMixin, Handler):

    _param_map = {'model':           (str,    'default',   facenet.MTCNN_MODEL_LIST),
                  'dim':             (int,    160,         None),
                  'margin':          (int,    32,          None),
                  'gpu_memory_frac': ((float, type(None)), None, None)}

    _keep_label, _keep_position = True, True

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._detector = None

    def prepare(self):

        self._detector = facenet.Detection(
            facenet.MTCNN_MODEL_PATH + self._model,
            self._dim, self._margin,
            self._gpu_memory_frac
        )

        self.execute_one(np.zeros((self._dim, self._dim, 3), dtype='uint8'))

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes = Boxes()

        result = self._detector.find_faces(rgb)

        for (x1, y1, x2, y2), crop in result:

            x, y, w, h = x1, y1, x2 - x1, y2 - y1

            boxes.append(Box('face', None, x, y, w, h, crop, match_size=False))

        return boxes

    def finish(self):

        pass
