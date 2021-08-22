import cv2

import openface

from .        import Handler
from .formats import Box, Boxes, BoxesInOutMixin


class DlibAlignHandler(BoxesInOutMixin, Handler):

    _param_map = {'predictor': (str, 'shape_predictor_68_face_landmarks.dat', openface.PREDICTOR_LIST),
                  'indices':   (str, 'OUTER_EYES_AND_NOSE', openface.AlignDlib.INDICES_LIST),
                  'dim':       (int, 96,                    None)}

    _keep_label, _keep_position = True, True

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._aligner   = None
        self._landmarks = None

    def prepare(self):

        self._aligner = openface.AlignDlib(
            openface.PREDICTOR_PATH + self._predictor
        )

        self._landmarks = openface.AlignDlib.get_indices(self._indices)

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        aligned = self._aligner.align(rgb, self._dim, self._landmarks)

        if aligned is None: return Boxes()

        aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)

        box = Box(crop=aligned, match_size=False)

        return Boxes([box])

    def finish(self):

        pass
