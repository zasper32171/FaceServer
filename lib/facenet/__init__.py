import os

from .face import *


def _get_list_from_path(path, type='f'):
    if type == 'f':
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    elif type == 'd':
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    else:
        return []


MTCNN_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'mtcnn', '')
FACENET_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'facenet', '')
CLASSIFIER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'classifier', '')

FACENET_MODEL_LIST = _get_list_from_path(FACENET_MODEL_PATH, 'd')
MTCNN_MODEL_LIST = _get_list_from_path(MTCNN_MODEL_PATH, 'd')
CLASSIFIER_LIST = _get_list_from_path(CLASSIFIER_PATH)
