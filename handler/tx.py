import socket
import pickle
import time

from . import BufferedData, Handler


MAX_BUF_SIZE = 65507


class TxHandler(Handler):

    _param_map = {'addr':     (str, '',    None),
                  'port':     (int, 0,     None),
                  'protocol': (str, 'udp', ['udp', 'tcp'])}

    _num_input, _num_output = 1, 0

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._socket = None

    def prepare(self):

        if self._protocol == 'udp':

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(('', 0))

        elif self._protocol == 'tcp':

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(('', 0))

            while True:
                try:
                    self._socket.connect((self._addr, self._port))

                except ConnectionRefusedError:
                    continue

                else: break
        else:
            raise Exception('Unknow protocol type(%s).' % self._protocol)

    def execute(self, packet):

        packet = pickle.dumps(BufferedData(self._sequence, packet))

        if self._protocol == 'udp':

            sent = 0

            while True:

                segment = packet[sent: min(sent + MAX_BUF_SIZE, len(packet))]
                sent += self._socket.sendto(segment, (self._addr, self._port))

                if sent >= len(packet): break

            self._socket.sendto(bytes(), (self._addr, self._port))

        elif self._protocol == 'tcp':

            self._socket.sendall(len(packet).to_bytes(4, byteorder="big"))
            self._socket.sendall(packet)

        else:
            raise Exception('Unknow protocol type(%s).' % self._protocol)

        if self._report_sink:
            timestamp = time.time()

            report = {'handler_id': self.id,
                      'timestamp':  timestamp,
                      'sequence':   self._sequence,
                      'event':      'send',
                      'size':       len(packet)}

            self._report_sink.put(report)

    def finish(self):

        self._socket.close()
