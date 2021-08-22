import threading
import queue
import socket
import time

import cv2 as cv
import numpy


LOCAL_ADDR   = 'localhost'
LOCAL_PORT   = 9002

SERVER_ADDR  = '140.112.20.181'
SERVER_PORT  = 9000

MAX_BUF_SIZE = 65507


def receive(terminate, output_buf):

    rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rx_socket.bind((LOCAL_ADDR, LOCAL_PORT))
    rx_socket.settimeout(1.0)

    while not terminate.is_set():
        try:
            packet = bytes()
            while True:
                data, _ = rx_socket.recvfrom(1 << 16)
                if not data: break
                packet += data

        except socket.timeout:
            continue

        output_buf.put(packet)

    rx_socket.close()


def send(terminate, input_buf):

    tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx_socket.bind((LOCAL_ADDR, 0))
    tx_socket.settimeout(1.0)

    while not terminate.is_set():

        data = input_buf.get()

        try:
            start = 0
            while True:
                end = min(start + MAX_BUF_SIZE, len(data))
                start += tx_socket.sendto(data[start: end], (SERVER_ADDR, SERVER_PORT))
                if start >= len(data): break
            ret = tx_socket.sendto(bytes(), (SERVER_ADDR, SERVER_PORT))
            
        except socket.timeout:
            continue
            
        except socket.gaierror:
            print("Error: Unkown host (" + SERVER_ADDR + ").")
            terminate.set()

    tx_socket.close()


def encode(terminate, input_buf, output_buf):

    while not terminate.is_set():

        frame = input_buf.get()

        _, encoded = cv.imencode('.jpg', frame, (cv.IMWRITE_JPEG_QUALITY, 80))

        data = encoded.tostring()

        output_buf.put(data)


def decode(terminate, input_buf, output_buf):

    while not terminate.is_set():

        data = input_buf.get()

        encoded = numpy.fromstring(data, dtype='uint8')
        frame = cv.imdecode(encoded, cv.IMREAD_COLOR)

        output_buf.put(frame)


def capture(terminate, output_buf):

    cam = cv.VideoCapture(0)

    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    while not terminate.is_set():

        ret, frame = cam.read()
        while ret is not True:
            ret, frame = cam.read()

        output_buf.put(frame)

        time.sleep(0.03)

    cam.release()


def render(terminate, input_buf):

    while not terminate.is_set():

        result = input_buf.get()

        cv.imshow('camera', result)
        cv.waitKey(1)

    cv.destroyAllWindows()


def main():

    try:
        threads = []

        terminate = threading.Event()

        enc_buf  = queue.Queue()
        tx_buf   = queue.Queue()
        dec_buf  = queue.Queue()
        rend_buf = queue.Queue()

        threads.append(threading.Thread(
            target=capture,
            args=(terminate, enc_buf,)))

        threads.append(threading.Thread(
            target=encode,
            args=(terminate, enc_buf, tx_buf,)))

        threads.append(threading.Thread(
            target=send,
            args=(terminate, tx_buf,)))

        threads.append(threading.Thread(
            target=receive,
            args=(terminate, dec_buf,)))

        threads.append(threading.Thread(
            target=decode,
            args=(terminate, dec_buf, rend_buf,)))

        threads.append(threading.Thread(
            target=render,
            args=(terminate, rend_buf,)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    except (KeyboardInterrupt, SystemExit):

        terminate.set()


if __name__ == '__main__':

    main()

