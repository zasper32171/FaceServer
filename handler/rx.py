import socket
import pickle
import time

from . import Handler


MAX_BUF_SIZE = 65536


class RxHandler(Handler):

    _param_map = {'addr':     (str, '',    None),
                  'port':     (int, 0,     None),
                  'protocol': (str, 'udp', ['udp', 'tcp'])}

    _num_input, _num_output = 0, 1

    def __init__(self, hid, name='', params=None):

        super().__init__(hid, name=name, params=params)

        self._socket = None
        self._conn   = None
        self._buffer = None

    def prepare(self):

        if self._protocol == 'udp':

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self._addr, self._port))

        elif self._protocol == 'tcp':

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self._addr, self._port))
            self._socket.listen()

            self._conn, _ = self._socket.accept()

        else:
            raise Exception('Unknow protocol type(%s).' % self._protocol)

    def execute(self):

        while True:

            packet = bytes()

            if self._protocol == 'udp':

                while True:

                    segment, _ = self._socket.recvfrom(MAX_BUF_SIZE)
                    if not segment:
                        break
                    packet += segment

            elif self._protocol == 'tcp':

                if not self._buffer:
                    length = int.from_bytes(self._conn.recv(4), byteorder="big")
                else:
                    length = int.from_bytes(self._buffer[:4], byteorder="big")
                    packet += self._buffer[4:]
                    self._buffer = bytes()

                while len(packet) < length:
                    segment = self._conn.recv(MAX_BUF_SIZE)
                    packet += segment

                if len(packet) > length:
                    self._buffer = packet[length:]
                    packet = packet[:length]

            else:
                raise Exception('Unknow protocol type(%s).' % self._protocol)

            try:
                data = pickle.loads(packet)

            except (pickle.PickleError, EOFError):
                print('Packet corrupted.')

            else: break

        if self._report_sink:

            timestamp = time.time()

            report = {'handler_id': self.id,
                      'timestamp':  timestamp,
                      'sequence':   data.sequence,
                      'event':      'receive',
                      'size':       len(packet)}

            self._report_sink.put(report)

        return data

    def finish(self):

        if self._protocol == 'tcp':
            self._conn.close()

        self._socket.close()
