import threading
import queue
import socket
import time

import cv2 as cv
import numpy


LOCAL_ADDR  = 'localhost'
LOCAL_PORT  = 9000

CLIENT_ADDR = '140.112.20.184'
CLIENT_PORT = 9002


def receive(terminate, output_buf):

    rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rx_socket.bind((LOCAL_ADDR, LOCAL_PORT))
    rx_socket.settimeout(1.0)

    while not terminate.is_set():
        try:
            data, _ = rx_socket.recvfrom(1 << 20)
        except socket.timeout:
            continue

        output_buf.put(data)

    rx_socket.close()


def send(terminate, input_buf):

    tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx_socket.bind((LOCAL_ADDR, 0))
    tx_socket.settimeout(1.0)

    while not terminate.is_set():

        data = input_buf.get()

        try:
            tx_socket.sendto(data, (CLIENT_ADDR, CLIENT_PORT))
        except socket.timeout:
            continue
        except socket.gaierror:
            print("Error: Unkown host (" + CLIENT_ADDR + ").")
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


def detect(terminate, input_buf, output_buf):

    detector = cv.CascadeClassifier(
        cv.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    period, count = 2, 0

    while not terminate.is_set():

        result = input_buf.get()

        if count == 0:

            gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
            gray = cv.equalizeHist(gray)
            faces = detector.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=3, minSize=(40, 40),
                flags=cv.CASCADE_SCALE_IMAGE
            )

        for (x, y, w, h) in faces:
            cv.rectangle(result, (x, y), (x + w, y + h), (0, 255, 255), 2)

        output_buf.put(result)

        count += 1
        if count >= period:
            count = 0


def main():

    try:
        threads = []

        terminate = threading.Event()

        rx_buf  = queue.Queue()
        dec_buf = queue.Queue()
        enc_buf = queue.Queue()
        tx_buf  = queue.Queue()

        threads.append(threading.Thread(
            target=receive,
            args=(terminate, rx_buf,)))

        threads.append(threading.Thread(
            target=decode,
            args=(terminate, rx_buf, dec_buf,)))

        threads.append(threading.Thread(
            target=detect,
            args=(terminate, dec_buf, enc_buf,)))

        threads.append(threading.Thread(
            target=encode,
            args=(terminate, enc_buf, tx_buf,)))

        threads.append(threading.Thread(
            target=send,
            args=(terminate, tx_buf,)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    except (KeyboardInterrupt, SystemExit):

        terminate.set()


if __name__ == '__main__':

    main()

