import multiprocessing as mp
import threading
import time

from handler import new_handler


#mp.set_start_method('spawn')


class ParseError(Exception):

    pass


class InitError(Exception):

    pass


class Session:

    def __init__(self, sid, blueprint):

        self.id = sid

        self._blueprint   = blueprint

        self._handlers    = []

        self._report_sink = mp.Queue()

        self.initialized  = threading.Event()
        self.running      = threading.Event()
        self.terminating  = threading.Event()
        self.terminated   = threading.Event()

    def init(self, timeout=30):

        assert not self.initialized.is_set()

        try:
            for h in self._blueprint['handlers']:

                if self.get_handler(h['handler_id']) is not None:
                    raise ParseError('Handler id duplicated.')

                handler = new_handler(
                    h['handler_id'],
                    h['handler_name'],
                    h['handler_type'],
                    h['params']
                )

                self._handlers.append(handler)

            for l in self._blueprint['links']:

                source = self.get_handler(l['source_handler'])
                source_output = l['source_output']

                target = self.get_handler(l['target_handler'])
                target_input = l['target_input']

                source.append_output(source_output, target, target_input)

            for h in self._handlers:

                h.add_report_sink(self._report_sink)

            for h in self._handlers:

                try:
                    h.init(block=False)

                except Exception as e:
                    raise InitError(e)

            deadline = time.time() + timeout

            for h in self._handlers:

                if deadline >= time.time():
                    h.initialized.wait(deadline - time.time())

                else:
                    raise InitError(
                        'Init process takes too long (%fs).' % timeout)

            for h in self._handlers:

                if not h.is_alive():
                    raise InitError('Handler (%d) exits unexpectively.' % h.id)

        except KeyError as e:
            raise ParseError(e)

        else:
            self.initialized.set()

    def deinit(self):

        assert not self.running.is_set()
        assert not self.terminated.is_set()

        for h in self._handlers:
            h.deinit()

        self.terminated.set()

    def get_handler(self, hid):

        result = [h for h in self._handlers if h.id == hid]

        assert len(result) <= 1

        return result[0] if result else None

    def get_handlers(self):

        return self._handlers

    def get_report_sink(self):

        return self._report_sink

    def start(self):

        assert self.initialized.is_set()
        assert not self.running.is_set()
        assert not self.terminated.is_set()

        for h in self._handlers:
            h.start()

        self.running.set()

    def stop(self, timeout=10):

        assert self.running.is_set()

        self.terminating.set()

        for h in self._handlers:
            h.stop(block=False)

        deadline = time.time() + timeout

        for h in self._handlers:

            if deadline >= time.time():
                h.terminated.wait(deadline - time.time())

            h.terminate()

        self.terminating.clear()
        self.running.clear()
        self.terminated.set()
