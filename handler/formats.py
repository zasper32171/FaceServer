import numpy


class FormatError(Exception):
    pass


Frame = numpy.ndarray


class Box():

    def __init__(self, label=None, prob=None, x=0, y=0, w=0, h=0, crop=None,
                 match_size=True):

        assert x >= 0 and y >= 0

        if crop is not None:
            assert isinstance(crop, Frame)

            if match_size:
                crop_h, crop_w, _ = crop.shape

                if not (w == 0 and h == 0):
                    assert w == crop_w and h == crop_h
                else:
                    w, h = crop_w, crop_h

        self.label      = label
        self.prob       = prob
        self.x          = x
        self.y          = y
        self.w          = w
        self.h          = h
        self.crop       = crop
        self.match_size = match_size


class Boxes(list):

    def __init__(self, arg=None):

        if arg is None:

            super().__init__([])

        else:
            assert isinstance(arg, (Boxes)) or \
                (isinstance(arg, list) and all([isinstance(e, Box) for e in arg]))

            super().__init__(arg)

    def append(self, value):

        assert isinstance(value, Box)
        super().append(value)

    def __setitem__(self, key, value):

        assert isinstance(value, Box)
        super().__setitem__(key, value)

    def largest(self):

        if all(box.prob is not None for box in self):
            largest = max(self, key=lambda box: box.prob)
        else:
            largest = max(self, key=lambda box: box.w * box.h)

        return largest


class BoxesInOutMixin:

    _param_map = {'with_crop':    (bool, True, None),
                  'multiple':     (bool, True, None)}

    _num_input, _num_output = 1, 1

    _keep_label, _keep_position = False, False

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

    def execute_one(self, frame):

        raise NotImplementedError

    def execute(self, data):

        if isinstance(data, Frame):

            boxes = self.execute_one(data)

            assert isinstance(boxes, Boxes)

            if not self._multiple:
                boxes = Boxes([boxes.largest()])

            for box in boxes:
                if not self._with_crop: box.crop = None

        elif isinstance(data, Boxes):

            boxes = Boxes()

            for b in data:
                result = self.execute_one(b.crop)

                assert isinstance(result, Boxes)

                if not self._multiple:
                    result = Boxes([result.largest()])

                for box in result:
                    if self._keep_label:
                        box.label = b.label

                    if self._keep_position:
                        box.x, box.y, box.w, box.h = b.x, b.y, b.w, b.h
                    else:
                        box.x, box.y = b.x + box.x, b.y + box.y

                    if not self._with_crop:
                        box.crop = None

                    boxes.append(box)
        else:
            raise FormatError('Unknown input type (%s)' % type(data))

        return boxes
