import ctypes
import cv2

import darknet

from .        import Handler
from .formats import Box, Boxes, BoxesInOutMixin


class YoloDetectObjectHandler(BoxesInOutMixin, Handler):

    _param_map = {'gpu':         (bool,   True,                  None),
                  'config':      (str,    'yolov3-tiny-416.cfg', darknet.CONFIG_LIST),
                  'weights':     (str,    'yolov3-tiny.weights', darknet.WEIGHTS_LIST),
                  'labels':      (str,    'coco.names',          darknet.LABEL_LIST),
                  'targets':     (list,   ['all'],               None),
                  'thresh':      (float,  0.5,                   None),
                  'hier_thresh': (float,  0.5,                   None),
                  'nms':         (float,  0.45,                  None)}

    _num_input, _num_output = 1, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._net     = None
        self._names   = []
        self._classes = 0

    def prepare(self):

        if self._gpu:
            darknet.cuda_set_device(0)
        else:
            darknet.gpu_index = -1

        self._net = darknet.load_network(
            darknet.CONFIG_PATH + self._config,
            darknet.WEIGHTS_PATH + self._weights,
            0
        )

        with open(darknet.LABEL_PATH + self._labels) as f:
            self._names = [l.strip() for l in f if l.strip()]

        self._classes = len(self._names)

    def execute_one(self, frame):

        if frame is None:
            print('Warning: got empty frame.')
            return Boxes()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = darknet.array_to_image(rgb)

        darknet.network_predict_image(self._net, rgb)

        nboxes = ctypes.c_int(0)
        dets = darknet.get_network_boxes(
            self._net, rgb.w, rgb.h, self._thresh,
            self._hier_thresh, None, 1, ctypes.byref(nboxes)
        )

        if self._nms:
            darknet.do_nms_obj(dets, nboxes.value, self._classes, self._nms)

        boxes = Boxes()

        for i in range(nboxes.value):
            for j in range(self._classes):

                name = self._names[j]
                bbox = dets[i].bbox
                prob = dets[i].prob[j]

                if not self._targets == ['all'] and name not in self._targets:
                    continue

                if prob <= 0:
                    continue

                x = round((bbox.x - bbox.w / 2) * rgb.w)
                y = round((bbox.y - bbox.h / 2) * rgb.h)
                w = round(bbox.w * rgb.w)
                h = round(bbox.h * rgb.h)

                x = min(max(x, 0), rgb.w)
                y = min(max(y, 0), rgb.h)
                w = min(max(w, 0), rgb.w - x)
                h = min(max(h, 0), rgb.h - y)

                crop = frame[y: y + h, x: x + w]

                # print(self._names[j], prob, x, y, w, h)
                boxes.append(Box(name, prob, x, y, w, h, crop))

        # darknet.free_image(rgb)
        darknet.free_detections(dets, nboxes)

        return boxes

    def finish(self):

        darknet.free_network(self._net)
