import os


def _get_list_from_path(path, type='f'):
    if type == 'f':
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    elif type == 'd':
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    else:
        return []


DETECTOR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'detector', '')
PREDICTOR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'predictor', '')
MODEL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models', '')
CLASSIFIER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'classifier', '')

DETECTOR_LIST  = _get_list_from_path(DETECTOR_PATH)
PREDICTOR_LIST  = _get_list_from_path(PREDICTOR_PATH)
MODEL_LIST = _get_list_from_path(MODEL_PATH)
CLASSIFIER_LIST = _get_list_from_path(CLASSIFIER_PATH)
