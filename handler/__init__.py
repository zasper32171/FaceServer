import multiprocessing as mp
import heapq
import time


def new_handler(hid, name, tid, params):

    from .tx                import TxHandler                    # 0
    from .rx                import RxHandler                    # 1
    from .capture           import CaptureHandler               # 2
    from .render            import RenderHandler                # 3
    from .resize            import ResizeHandler                # 4
    from .encode            import EncodeHandler                # 5
    from .decode            import DecodeHandler                # 6
    from .detect_object     import YoloDetectObjectHandler      # 7
    from .detect_face       import HaarDetectFaceHandler        # 8
    from .detect_face       import HogDetectFaceHandler         # 9
    from .detect_face       import MmodDetectFaceHandler        # 10
    from .align             import DlibAlignHandler             # 11
    from .detect_face_align import MtcnnDetectFaceAlignHandler  # 12
    from .align_recognize   import DlibAlignRecognizeHandler    # 13
    from .recognize         import OpenfaceRecognizeHandler     # 14
    from .recognize         import FacenetRecognizeHandler      # 15
    from .draw              import DrawBoxesHandler             # 16
    from .draw              import DrawLabeledBoxesHandler      # 17

    handler_type_list = [
        TxHandler,
        RxHandler,
        CaptureHandler,
        RenderHandler,
        ResizeHandler,
        EncodeHandler,
        DecodeHandler,
        YoloDetectObjectHandler,
        HaarDetectFaceHandler,
        HogDetectFaceHandler,
        MmodDetectFaceHandler,
        DlibAlignHandler,
        MtcnnDetectFaceAlignHandler,
        DlibAlignRecognizeHandler,
        OpenfaceRecognizeHandler,
        FacenetRecognizeHandler,
        DrawBoxesHandler,
        DrawLabeledBoxesHandler
    ]

    return handler_type_list[tid](hid, name, params)


class BufferedData:

    def __init__(self, sequence, data):

        self.sequence = sequence
        self.data     = data


MAX_CACHE_SIZE = 4
MAX_QUEUE_SIZE = 1024


class Handler(mp.Process):

    _param_map = {}

    _num_input, _num_output = 0, 0

    def __init__(self, hid, name='', params=None):

        mp.Process.__init__(
            self, daemon=True
        )

        self.id       = hid
        self.name     = name

        self._options = {}

        for cls in reversed(self.__class__.__mro__):
            if hasattr(cls, '_param_map'):
                self._options.update(cls._param_map)

        self._params = params if params else {}

        for key in self._params:
            if key not in self._options:
                print('Warning: unknow parameter(%s)' % key)

        for key, (vtype, default, vrange) in self._options.items():

            value = self._params[key] if key in self._params else default

            assert isinstance(value, vtype)
            assert vrange is None or value in vrange

            setattr(self, '_' + key, value)

        self._input       = []
        self._input_cache = []
        self._input_buf   = []
        self._output      = []
        self._output_buf  = []

        for _ in range(self._num_input):
            self._input.append(mp.Queue(MAX_QUEUE_SIZE))

        for _ in range(self._num_input):
            self._input_cache.append([])

        for _ in range(self._num_output):
            self._output.append([])

        self._sequence    = 0

        self._report_sink = None

        self.initialized  = mp.Event()
        self.running      = mp.Event()
        self.terminating  = mp.Event()
        self.terminated   = mp.Event()

    def get_input(self, input_id):

        assert input_id < self._num_input

        return self._input[input_id]

    def get_output(self, output_id):

        assert output_id < self._num_output

        return self._output[output_id]

    def append_input(self, input_id, handler, output_id):

        assert not self.initialized.is_set()
        assert input_id < self._num_input

        source = handler.get_output(output_id)
        source.append(self._input[input_id])

    def append_output(self, output_id, handler, input_id):

        assert not self.initialized.is_set()
        assert output_id < self._num_output

        target = handler.get_input(input_id)
        self._output[output_id].append(target)

    def add_report_sink(self, sink):

        assert not self.initialized.is_set()
        self._report_sink = sink

    def init(self, block=True, timeout=None):

        assert not self.initialized.is_set()
        assert not self.terminated.is_set()

        mp.Process.start(self)

        if block and not self.initialized.wait(timeout):
            if self.is_alive():
                self.terminate()
            return False

        return True

    def deinit(self):

        assert not self.running.is_set()
        assert not self.terminated.is_set()

        if self.is_alive():
            self.terminate()

        self.initialized.clear()
        self.terminated.set()

    def pull_input_sync(self, input_id):

        assert input_id < self._num_input
        assert len(self._input_buf) == self._num_input

        cache = self._input_cache[input_id]
        queue = self._input[input_id]

        while cache and cache[0][0] <= self._sequence:

            sequence, data = heapq.heappop(cache)

            if sequence == self._sequence:
                self._input_buf[input_id] = data.data
                return True

        while len(cache) < MAX_CACHE_SIZE:

            # TODO: stop blocking after some waiting time?
            # TODO: quit blocking when terminating is set
            data = queue.get()
            sequence = data.sequence

            if sequence == self._sequence:
                self._input_buf[input_id] = data.data
                return True

            if sequence > self._sequence:
                heapq.heappush(cache, (sequence, data))

        return False

    def pull_inputs_sync(self):

        for input_id in range(self._num_input):
            if not self.pull_input_sync(input_id):
                return False

        assert all([data is not None for data in self._input_buf])

        return True

    def pull_inputs(self):

        self.clear_input_buf()

        # Not sync, not in-order way:
        #     self._input_buf = [q.get() for q in self._input]

        while not self.pull_inputs_sync():
            self._sequence += 1

        assert len(self._input_buf) == self._num_input

        if self._report_sink:

            report = {'handler_id': self.id,
                      'timestamp':  time.time(),
                      'sequence':   self._sequence,
                      'event':      'start'}

            self._report_sink.put(report)

    def push_outputs(self):

        if self._report_sink:
            timestamp = time.time()

            report = {'handler_id': self.id,
                      'timestamp':  timestamp,
                      'sequence':   self._sequence,
                      'event':      'end'}

            self._report_sink.put(report)

        assert len(self._output_buf) == self._num_output

        for output_id, data in enumerate(self._output_buf):
            if not isinstance(data, BufferedData):
                data = BufferedData(self._sequence, data)
                self._output_buf[output_id] = data

        # TODO: handle when queue is full
        for link in zip(self._output, self._output_buf):
            for q in link[0]:
                q.put(link[1])

        self._sequence += 1

        self.clear_output_buf()

    def clear_input_buf(self):

        self._input_buf = [None] * self._num_input

    def clear_output_buf(self):

        self._output_buf = [None] * self._num_output

    def prepare(self):

        raise NotImplementedError

    def execute(self):

        raise NotImplementedError

    def finish(self):

        raise NotImplementedError

    def run(self):

        self.prepare()

        self.initialized.set()
        self.running.wait()

        while not self.terminating.is_set():

            self.pull_inputs()

            # TODO: handle input/output format error?
            ret = self.execute(*self._input_buf)

            if ret is None:
                self._output_buf = []

            elif isinstance(ret, tuple):
                self._output_buf = list(ret)

            else:
                self._output_buf = [ret]

            self.push_outputs()

        for link in self._output:
            for q in link:
                q.close()

        self.finish()

        self.initialized.clear()
        self.running.clear()
        self.terminating.clear()
        self.terminated.set()

    def start(self):

        assert self.initialized.is_set()
        assert not self.running.is_set()

        self.running.set()

    def stop(self, block=True, timeout=None):

        assert self.running.is_set()

        self.terminating.set()

        if block:
            self.terminated.wait(timeout)
            self.terminate()
