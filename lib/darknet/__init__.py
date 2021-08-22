import os

from .darknet import *


def _get_list_from_path(path, type='f'):
    if type == 'f':
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    elif type == 'd':
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    else:
        return []


CONFIG_PATH  = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg', '')
WEIGHTS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weights', '')
LABEL_PATH   = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'label', '')

CONFIG_LIST  = _get_list_from_path(CONFIG_PATH)
WEIGHTS_LIST = _get_list_from_path(WEIGHTS_PATH)
LABEL_LIST   = _get_list_from_path(LABEL_PATH)
