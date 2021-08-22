import os

from .align_dlib import AlignDlib
from .torch_neural_net import TorchNeuralNet


def _get_list_from_path(path, type='f'):
    if type == 'f':
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    elif type == 'd':
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    else:
        return []


PREDICTOR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models', 'dlib', '')
MODEL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models', 'openface', '')
CLASSIFIER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models', 'classifier', '')

PREDICTOR_LIST  = _get_list_from_path(PREDICTOR_PATH)
MODEL_LIST = _get_list_from_path(MODEL_PATH)
CLASSIFIER_LIST = _get_list_from_path(CLASSIFIER_PATH)
