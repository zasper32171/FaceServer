import time
import sys

from config import ConfigReader


sys.path.append('./lib')


def usage():

    print('Usage: python3 main.py <config>')


def error():

    usage()
    exit()


def main():

    if len(sys.argv) != 2:
        error()

    conf = ConfigReader(sys.argv[1])
    manager = conf.init_manager()

    try:
        manager.start()

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:

        manager.stop()


if __name__ == '__main__':

    main()
