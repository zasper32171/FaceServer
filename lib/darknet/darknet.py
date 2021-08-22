import os
import sys
import numpy as np
from ctypes import *


class String(Union):

    @classmethod
    def from_param(cls, obj):
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())
        elif isinstance(obj, (bytes, bytearray)):
            return obj
        elif isinstance(obj, (c_char_p, POINTER(c_char))):
            return obj
        elif isinstance(obj, str):
            return bytes(obj, 'utf-8')
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))
        else:
            return String.from_param(obj._as_parameter_)
            
def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

_darknet = cdll.LoadLibrary(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libdarknet.so'))

def array_to_image(array):
    h, w, c = array.shape
    array = (array / 255).transpose(2,0,1).flatten().astype(np.float32)
    data = (c_float * len(array)).from_buffer(array)
    image = struct_image(w, h, c, data)
    return image


gpu_index = (c_int).in_dll(_darknet, 'gpu_index')


ACTIVATION              = c_int
LOGISTIC                = 0
RELU                    = 1
RELIE                   = 2
LINEAR                  = 3
RAMP                    = 4
TANH                    = 5
PLSE                    = 6
LEAKY                   = 7
ELU                     = 8
LOGGY                   = 9
STAIR                   = 10
HARDTAN                 = 11
LHTAN                   = 12
SELU                    = 13

IMTYPE                  = c_int
PNG                     = 0
BMP                     = 1
TGA                     = 2
JPG                     = 3

BINARY_ACTIVATION       = c_int
MULT                    = 0
ADD                     = 1
SUB                     = 2
DIV                     = 3

LAYER_TYPE              = c_int
CONVOLUTIONAL           = 0
DECONVOLUTIONAL         = 1
CONNECTED               = 2
MAXPOOL                 = 3
SOFTMAX                 = 4
DETECTION               = 5
DROPOUT                 = 6
CROP                    = 7
ROUTE                   = 8
COST                    = 9
NORMALIZATION           = 10
AVGPOOL                 = 11
LOCAL                   = 12
SHORTCUT                = 13
ACTIVE                  = 14
RNN                     = 15
GRU                     = 16
LSTM                    = 17
CRNN                    = 18
BATCHNORM               = 19
NETWORK                 = 20
XNOR                    = 21
REGION                  = 22
YOLO                    = 23
ISEG                    = 24
REORG                   = 25
UPSAMPLE                = 26
LOGXENT                 = 27
L2NORM                  = 28
BLANK                   = 29

COST_TYPE               = c_int
SSE                     = 0
MASKED                  = 1
L1                      = 2
SEG                     = 3
SMOOTH                  = 4
WGAN                    = 5

learning_rate_policy    = c_int
CONSTANT                = 0
STEP                    = 1
EXP                     = 2
POLY                    = 3
STEPS                   = 4
SIG                     = 5
RANDOM                  = 6

data_type               = c_int
CLASSIFICATION_DATA     = 0 
DETECTION_DATA          = 1
CAPTCHA_DATA            = 2
REGION_DATA             = 3
IMAGE_DATA              = 4
COMPARE_DATA            = 5
WRITING_DATA            = 6
SWAG_DATA               = 7
TAG_DATA                = 8
OLD_CLASSIFICATION_DATA = 9
STUDY_DATA              = 10
DET_DATA                = 11
SUPER_DATA              = 12
LETTERBOX_DATA          = 13
REGRESSION_DATA         = 14
SEGMENTATION_DATA       = 15
INSTANCE_DATA           = 16
ISEG_DATA               = 17


class struct_metadata(Structure):
    pass

struct_metadata.__slots__ = [
    'classes',
    'names',
]

struct_metadata._fields_ = [
    ('classes', c_int),
    ('names', POINTER(c_char_p)),
]

get_metadata = _darknet.get_metadata
get_metadata.argtypes = [String]
get_metadata.restype = struct_metadata


class struct_tree(Structure):
    pass

struct_tree.__slots__ = [
    'leaf',
    'n',
    'parent',
    'child',
    'group',
    'name',
    'groups',
    'group_size',
    'group_offset',
]

struct_tree._fields_ = [
    ('leaf', POINTER(c_int)),
    ('n', c_int),
    ('parent', POINTER(c_int)),
    ('child', POINTER(c_int)),
    ('group', POINTER(c_int)),
    ('name', POINTER(c_char_p)),
    ('groups', c_int),
    ('group_size', POINTER(c_int)),
    ('group_offset', POINTER(c_int)),
]

read_tree = _darknet.read_tree
read_tree.argtypes = [String]
read_tree.restype = POINTER(struct_tree)


class struct_update_args(Structure):
    pass

struct_update_args.__slots__ = [
    'batch',
    'learning_rate',
    'momentum',
    'decay',
    'adam',
    'B1',
    'B2',
    'eps',
    't',
]

struct_update_args._fields_ = [
    ('batch', c_int),
    ('learning_rate', c_float),
    ('momentum', c_float),
    ('decay', c_float),
    ('adam', c_int),
    ('B1', c_float),
    ('B2', c_float),
    ('eps', c_float),
    ('t', c_int),
]


class struct_network(Structure):
    pass

class struct_layer(Structure):
    pass

struct_network.__slots__ = [
    'n',
    'batch',
    'seen',
    't',
    'epoch',
    'subdivisions',
    'layers',
    'output',
    'policy',
    'learning_rate',
    'momentum',
    'decay',
    'gamma',
    'scale',
    'power',
    'time_steps',
    'step',
    'max_batches',
    'scales',
    'steps',
    'num_steps',
    'burn_in',
    'adam',
    'B1',
    'B2',
    'eps',
    'inputs',
    'outputs',
    'truths',
    'notruth',
    'h',
    'w',
    'c',
    'max_crop',
    'min_crop',
    'max_ratio',
    'min_ratio',
    'center',
    'angle',
    'aspect',
    'exposure',
    'saturation',
    'hue',
    'random',
    'gpu_index',
    'hierarchy',
    'input',
    'truth',
    'delta',
    'workspace',
    'train',
    'index',
    'cost',
    'clip',
    'input_gpu',
    'truth_gpu',
    'delta_gpu',
    'output_gpu',
]

struct_network._fields_ = [
    ('n', c_int),
    ('batch', c_int),
    ('seen', POINTER(c_size_t)),
    ('t', POINTER(c_int)),
    ('epoch', c_float),
    ('subdivisions', c_int),
    ('layers', POINTER(struct_layer)),
    ('output', POINTER(c_float)),
    ('policy', learning_rate_policy),
    ('learning_rate', c_float),
    ('momentum', c_float),
    ('decay', c_float),
    ('gamma', c_float),
    ('scale', c_float),
    ('power', c_float),
    ('time_steps', c_int),
    ('step', c_int),
    ('max_batches', c_int),
    ('scales', POINTER(c_float)),
    ('steps', POINTER(c_int)),
    ('num_steps', c_int),
    ('burn_in', c_int),
    ('adam', c_int),
    ('B1', c_float),
    ('B2', c_float),
    ('eps', c_float),
    ('inputs', c_int),
    ('outputs', c_int),
    ('truths', c_int),
    ('notruth', c_int),
    ('h', c_int),
    ('w', c_int),
    ('c', c_int),
    ('max_crop', c_int),
    ('min_crop', c_int),
    ('max_ratio', c_float),
    ('min_ratio', c_float),
    ('center', c_int),
    ('angle', c_float),
    ('aspect', c_float),
    ('exposure', c_float),
    ('saturation', c_float),
    ('hue', c_float),
    ('random', c_int),
    ('gpu_index', c_int),
    ('hierarchy', POINTER(struct_tree)),
    ('input', POINTER(c_float)),
    ('truth', POINTER(c_float)),
    ('delta', POINTER(c_float)),
    ('workspace', POINTER(c_float)),
    ('train', c_int),
    ('index', c_int),
    ('cost', POINTER(c_float)),
    ('clip', c_float),
    ('input_gpu', POINTER(c_float)),
    ('truth_gpu', POINTER(c_float)),
    ('delta_gpu', POINTER(c_float)),
    ('output_gpu', POINTER(c_float)),
]

load_network = _darknet.load_network
load_network.argtypes = [String, String, c_int]
load_network.restype = POINTER(struct_network)


struct_layer.__slots__ = [
    'type',
    'activation',
    'cost_type',
    'forward',
    'backward',
    'update',
    'forward_gpu',
    'backward_gpu',
    'update_gpu',
    'batch_normalize',
    'shortcut',
    'batch',
    'forced',
    'flipped',
    'inputs',
    'outputs',
    'nweights',
    'nbiases',
    'extra',
    'truths',
    'h',
    'w',
    'c',
    'out_h',
    'out_w',
    'out_c',
    'n',
    'max_boxes',
    'groups',
    'size',
    'side',
    'stride',
    'reverse',
    'flatten',
    'spatial',
    'pad',
    'sqrt',
    'flip',
    'index',
    'binary',
    'xnor',
    'steps',
    'hidden',
    'truth',
    'smooth',
    'dot',
    'angle',
    'jitter',
    'saturation',
    'exposure',
    'shift',
    'ratio',
    'learning_rate_scale',
    'clip',
    'noloss',
    'softmax',
    'classes',
    'coords',
    'background',
    'rescore',
    'objectness',
    'joint',
    'noadjust',
    'reorg',
    'log',
    'tanh',
    'mask',
    'total',
    'alpha',
    'beta',
    'kappa',
    'coord_scale',
    'object_scale',
    'noobject_scale',
    'mask_scale',
    'class_scale',
    'bias_match',
    'random',
    'ignore_thresh',
    'truth_thresh',
    'thresh',
    'focus',
    'classfix',
    'absolute',
    'onlyforward',
    'stopbackward',
    'dontload',
    'dontsave',
    'dontloadscales',
    'numload',
    'temperature',
    'probability',
    'scale',
    'cweights',
    'indexes',
    'input_layers',
    'input_sizes',
    'map',
    'counts',
    'sums',
    'rand',
    'cost',
    'state',
    'prev_state',
    'forgot_state',
    'forgot_delta',
    'state_delta',
    'combine_cpu',
    'combine_delta_cpu',
    'concat',
    'concat_delta',
    'binary_weights',
    'biases',
    'bias_updates',
    'scales',
    'scale_updates',
    'weights',
    'weight_updates',
    'delta',
    'output',
    'loss',
    'squared',
    'norms',
    'spatial_mean',
    'mean',
    'variance',
    'mean_delta',
    'variance_delta',
    'rolling_mean',
    'rolling_variance',
    'x',
    'x_norm',
    'm',
    'v',
    'bias_m',
    'bias_v',
    'scale_m',
    'scale_v',
    'z_cpu',
    'r_cpu',
    'h_cpu',
    'prev_state_cpu',
    'temp_cpu',
    'temp2_cpu',
    'temp3_cpu',
    'dh_cpu',
    'hh_cpu',
    'prev_cell_cpu',
    'cell_cpu',
    'f_cpu',
    'i_cpu',
    'g_cpu',
    'o_cpu',
    'c_cpu',
    'dc_cpu',
    'binary_input',
    'input_layer',
    'self_layer',
    'output_layer',
    'reset_layer',
    'update_layer',
    'state_layer',
    'input_gate_layer',
    'state_gate_layer',
    'input_save_layer',
    'state_save_layer',
    'input_state_layer',
    'state_state_layer',
    'input_z_layer',
    'state_z_layer',
    'input_r_layer',
    'state_r_layer',
    'input_h_layer',
    'state_h_layer',
    'wz',
    'uz',
    'wr',
    'ur',
    'wh',
    'uh',
    'uo',
    'wo',
    'uf',
    'wf',
    'ui',
    'wi',
    'ug',
    'wg',
    'softmax_tree',
    'workspace_size',
    'indexes_gpu',
    'z_gpu',
    'r_gpu',
    'h_gpu',
    'temp_gpu',
    'temp2_gpu',
    'temp3_gpu',
    'dh_gpu',
    'hh_gpu',
    'prev_cell_gpu',
    'cell_gpu',
    'f_gpu',
    'i_gpu',
    'g_gpu',
    'o_gpu',
    'c_gpu',
    'dc_gpu',
    'm_gpu',
    'v_gpu',
    'bias_m_gpu',
    'scale_m_gpu',
    'bias_v_gpu',
    'scale_v_gpu',
    'combine_gpu',
    'combine_delta_gpu',
    'prev_state_gpu',
    'forgot_state_gpu',
    'forgot_delta_gpu',
    'state_gpu',
    'state_delta_gpu',
    'gate_gpu',
    'gate_delta_gpu',
    'save_gpu',
    'save_delta_gpu',
    'concat_gpu',
    'concat_delta_gpu',
    'binary_input_gpu',
    'binary_weights_gpu',
    'mean_gpu',
    'variance_gpu',
    'rolling_mean_gpu',
    'rolling_variance_gpu',
    'variance_delta_gpu',
    'mean_delta_gpu',
    'x_gpu',
    'x_norm_gpu',
    'weights_gpu',
    'weight_updates_gpu',
    'weight_change_gpu',
    'biases_gpu',
    'bias_updates_gpu',
    'bias_change_gpu',
    'scales_gpu',
    'scale_updates_gpu',
    'scale_change_gpu',
    'output_gpu',
    'loss_gpu',
    'delta_gpu',
    'rand_gpu',
    'squared_gpu',
    'norms_gpu',
]

struct_layer._fields_ = [
    ('type', LAYER_TYPE),
    ('activation', ACTIVATION),
    ('cost_type', COST_TYPE),
    ('forward', CFUNCTYPE(c_void_p, struct_layer, struct_network)),
    ('backward', CFUNCTYPE(c_void_p, struct_layer, struct_network)),
    ('update', CFUNCTYPE(c_void_p, struct_layer, struct_update_args)),
    ('forward_gpu', CFUNCTYPE(c_void_p, struct_layer, struct_network)),
    ('backward_gpu', CFUNCTYPE(c_void_p, struct_layer, struct_network)),
    ('update_gpu', CFUNCTYPE(c_void_p, struct_layer, struct_update_args)),
    ('batch_normalize', c_int),
    ('shortcut', c_int),
    ('batch', c_int),
    ('forced', c_int),
    ('flipped', c_int),
    ('inputs', c_int),
    ('outputs', c_int),
    ('nweights', c_int),
    ('nbiases', c_int),
    ('extra', c_int),
    ('truths', c_int),
    ('h', c_int),
    ('w', c_int),
    ('c', c_int),
    ('out_h', c_int),
    ('out_w', c_int),
    ('out_c', c_int),
    ('n', c_int),
    ('max_boxes', c_int),
    ('groups', c_int),
    ('size', c_int),
    ('side', c_int),
    ('stride', c_int),
    ('reverse', c_int),
    ('flatten', c_int),
    ('spatial', c_int),
    ('pad', c_int),
    ('sqrt', c_int),
    ('flip', c_int),
    ('index', c_int),
    ('binary', c_int),
    ('xnor', c_int),
    ('steps', c_int),
    ('hidden', c_int),
    ('truth', c_int),
    ('smooth', c_float),
    ('dot', c_float),
    ('angle', c_float),
    ('jitter', c_float),
    ('saturation', c_float),
    ('exposure', c_float),
    ('shift', c_float),
    ('ratio', c_float),
    ('learning_rate_scale', c_float),
    ('clip', c_float),
    ('noloss', c_int),
    ('softmax', c_int),
    ('classes', c_int),
    ('coords', c_int),
    ('background', c_int),
    ('rescore', c_int),
    ('objectness', c_int),
    ('joint', c_int),
    ('noadjust', c_int),
    ('reorg', c_int),
    ('log', c_int),
    ('tanh', c_int),
    ('mask', POINTER(c_int)),
    ('total', c_int),
    ('alpha', c_float),
    ('beta', c_float),
    ('kappa', c_float),
    ('coord_scale', c_float),
    ('object_scale', c_float),
    ('noobject_scale', c_float),
    ('mask_scale', c_float),
    ('class_scale', c_float),
    ('bias_match', c_int),
    ('random', c_int),
    ('ignore_thresh', c_float),
    ('truth_thresh', c_float),
    ('thresh', c_float),
    ('focus', c_float),
    ('classfix', c_int),
    ('absolute', c_int),
    ('onlyforward', c_int),
    ('stopbackward', c_int),
    ('dontload', c_int),
    ('dontsave', c_int),
    ('dontloadscales', c_int),
    ('numload', c_int),
    ('temperature', c_float),
    ('probability', c_float),
    ('scale', c_float),
    ('cweights', String),
    ('indexes', POINTER(c_int)),
    ('input_layers', POINTER(c_int)),
    ('input_sizes', POINTER(c_int)),
    ('map', POINTER(c_int)),
    ('counts', POINTER(c_int)),
    ('sums', POINTER(POINTER(c_float))),
    ('rand', POINTER(c_float)),
    ('cost', POINTER(c_float)),
    ('state', POINTER(c_float)),
    ('prev_state', POINTER(c_float)),
    ('forgot_state', POINTER(c_float)),
    ('forgot_delta', POINTER(c_float)),
    ('state_delta', POINTER(c_float)),
    ('combine_cpu', POINTER(c_float)),
    ('combine_delta_cpu', POINTER(c_float)),
    ('concat', POINTER(c_float)),
    ('concat_delta', POINTER(c_float)),
    ('binary_weights', POINTER(c_float)),
    ('biases', POINTER(c_float)),
    ('bias_updates', POINTER(c_float)),
    ('scales', POINTER(c_float)),
    ('scale_updates', POINTER(c_float)),
    ('weights', POINTER(c_float)),
    ('weight_updates', POINTER(c_float)),
    ('delta', POINTER(c_float)),
    ('output', POINTER(c_float)),
    ('loss', POINTER(c_float)),
    ('squared', POINTER(c_float)),
    ('norms', POINTER(c_float)),
    ('spatial_mean', POINTER(c_float)),
    ('mean', POINTER(c_float)),
    ('variance', POINTER(c_float)),
    ('mean_delta', POINTER(c_float)),
    ('variance_delta', POINTER(c_float)),
    ('rolling_mean', POINTER(c_float)),
    ('rolling_variance', POINTER(c_float)),
    ('x', POINTER(c_float)),
    ('x_norm', POINTER(c_float)),
    ('m', POINTER(c_float)),
    ('v', POINTER(c_float)),
    ('bias_m', POINTER(c_float)),
    ('bias_v', POINTER(c_float)),
    ('scale_m', POINTER(c_float)),
    ('scale_v', POINTER(c_float)),
    ('z_cpu', POINTER(c_float)),
    ('r_cpu', POINTER(c_float)),
    ('h_cpu', POINTER(c_float)),
    ('prev_state_cpu', POINTER(c_float)),
    ('temp_cpu', POINTER(c_float)),
    ('temp2_cpu', POINTER(c_float)),
    ('temp3_cpu', POINTER(c_float)),
    ('dh_cpu', POINTER(c_float)),
    ('hh_cpu', POINTER(c_float)),
    ('prev_cell_cpu', POINTER(c_float)),
    ('cell_cpu', POINTER(c_float)),
    ('f_cpu', POINTER(c_float)),
    ('i_cpu', POINTER(c_float)),
    ('g_cpu', POINTER(c_float)),
    ('o_cpu', POINTER(c_float)),
    ('c_cpu', POINTER(c_float)),
    ('dc_cpu', POINTER(c_float)),
    ('binary_input', POINTER(c_float)),
    ('input_layer', POINTER(struct_layer)),
    ('self_layer', POINTER(struct_layer)),
    ('output_layer', POINTER(struct_layer)),
    ('reset_layer', POINTER(struct_layer)),
    ('update_layer', POINTER(struct_layer)),
    ('state_layer', POINTER(struct_layer)),
    ('input_gate_layer', POINTER(struct_layer)),
    ('state_gate_layer', POINTER(struct_layer)),
    ('input_save_layer', POINTER(struct_layer)),
    ('state_save_layer', POINTER(struct_layer)),
    ('input_state_layer', POINTER(struct_layer)),
    ('state_state_layer', POINTER(struct_layer)),
    ('input_z_layer', POINTER(struct_layer)),
    ('state_z_layer', POINTER(struct_layer)),
    ('input_r_layer', POINTER(struct_layer)),
    ('state_r_layer', POINTER(struct_layer)),
    ('input_h_layer', POINTER(struct_layer)),
    ('state_h_layer', POINTER(struct_layer)),
    ('wz', POINTER(struct_layer)),
    ('uz', POINTER(struct_layer)),
    ('wr', POINTER(struct_layer)),
    ('ur', POINTER(struct_layer)),
    ('wh', POINTER(struct_layer)),
    ('uh', POINTER(struct_layer)),
    ('uo', POINTER(struct_layer)),
    ('wo', POINTER(struct_layer)),
    ('uf', POINTER(struct_layer)),
    ('wf', POINTER(struct_layer)),
    ('ui', POINTER(struct_layer)),
    ('wi', POINTER(struct_layer)),
    ('ug', POINTER(struct_layer)),
    ('wg', POINTER(struct_layer)),
    ('softmax_tree', POINTER(struct_tree)),
    ('workspace_size', c_size_t),
    ('indexes_gpu', POINTER(c_int)),
    ('z_gpu', POINTER(c_float)),
    ('r_gpu', POINTER(c_float)),
    ('h_gpu', POINTER(c_float)),
    ('temp_gpu', POINTER(c_float)),
    ('temp2_gpu', POINTER(c_float)),
    ('temp3_gpu', POINTER(c_float)),
    ('dh_gpu', POINTER(c_float)),
    ('hh_gpu', POINTER(c_float)),
    ('prev_cell_gpu', POINTER(c_float)),
    ('cell_gpu', POINTER(c_float)),
    ('f_gpu', POINTER(c_float)),
    ('i_gpu', POINTER(c_float)),
    ('g_gpu', POINTER(c_float)),
    ('o_gpu', POINTER(c_float)),
    ('c_gpu', POINTER(c_float)),
    ('dc_gpu', POINTER(c_float)),
    ('m_gpu', POINTER(c_float)),
    ('v_gpu', POINTER(c_float)),
    ('bias_m_gpu', POINTER(c_float)),
    ('scale_m_gpu', POINTER(c_float)),
    ('bias_v_gpu', POINTER(c_float)),
    ('scale_v_gpu', POINTER(c_float)),
    ('combine_gpu', POINTER(c_float)),
    ('combine_delta_gpu', POINTER(c_float)),
    ('prev_state_gpu', POINTER(c_float)),
    ('forgot_state_gpu', POINTER(c_float)),
    ('forgot_delta_gpu', POINTER(c_float)),
    ('state_gpu', POINTER(c_float)),
    ('state_delta_gpu', POINTER(c_float)),
    ('gate_gpu', POINTER(c_float)),
    ('gate_delta_gpu', POINTER(c_float)),
    ('save_gpu', POINTER(c_float)),
    ('save_delta_gpu', POINTER(c_float)),
    ('concat_gpu', POINTER(c_float)),
    ('concat_delta_gpu', POINTER(c_float)),
    ('binary_input_gpu', POINTER(c_float)),
    ('binary_weights_gpu', POINTER(c_float)),
    ('mean_gpu', POINTER(c_float)),
    ('variance_gpu', POINTER(c_float)),
    ('rolling_mean_gpu', POINTER(c_float)),
    ('rolling_variance_gpu', POINTER(c_float)),
    ('variance_delta_gpu', POINTER(c_float)),
    ('mean_delta_gpu', POINTER(c_float)),
    ('x_gpu', POINTER(c_float)),
    ('x_norm_gpu', POINTER(c_float)),
    ('weights_gpu', POINTER(c_float)),
    ('weight_updates_gpu', POINTER(c_float)),
    ('weight_change_gpu', POINTER(c_float)),
    ('biases_gpu', POINTER(c_float)),
    ('bias_updates_gpu', POINTER(c_float)),
    ('bias_change_gpu', POINTER(c_float)),
    ('scales_gpu', POINTER(c_float)),
    ('scale_updates_gpu', POINTER(c_float)),
    ('scale_change_gpu', POINTER(c_float)),
    ('output_gpu', POINTER(c_float)),
    ('loss_gpu', POINTER(c_float)),
    ('delta_gpu', POINTER(c_float)),
    ('rand_gpu', POINTER(c_float)),
    ('squared_gpu', POINTER(c_float)),
    ('norms_gpu', POINTER(c_float)),
]

free_layer = _darknet.free_layer
free_layer.argtypes = [struct_layer]
free_layer.restype = None


class struct_augment_args(Structure):
    pass

struct_augment_args.__slots__ = [
    'w',
    'h',
    'scale',
    'rad',
    'dx',
    'dy',
    'aspect',
]

struct_augment_args._fields_ = [
    ('w', c_int),
    ('h', c_int),
    ('scale', c_float),
    ('rad', c_float),
    ('dx', c_float),
    ('dy', c_float),
    ('aspect', c_float),
]


class struct_image(Structure):
    pass

struct_image.__slots__ = [
    'w',
    'h',
    'c',
    'data',
]

struct_image._fields_ = [
    ('w', c_int),
    ('h', c_int),
    ('c', c_int),
    ('data', POINTER(c_float)),
]


class struct_box(Structure):
    pass

struct_box.__slots__ = [
    'x',
    'y',
    'w',
    'h',
]

struct_box._fields_ = [
    ('x', c_float),
    ('y', c_float),
    ('w', c_float),
    ('h', c_float),
]


class struct_detection(Structure):
    pass

struct_detection.__slots__ = [
    'bbox',
    'classes',
    'prob',
    'mask',
    'objectness',
    'sort_class',
]

struct_detection._fields_ = [
    ('bbox', struct_box),
    ('classes', c_int),
    ('prob', POINTER(c_float)),
    ('mask', POINTER(c_float)),
    ('objectness', c_float),
    ('sort_class', c_int),
]


class struct_matrix(Structure):
    pass

struct_matrix.__slots__ = [
    'rows',
    'cols',
    'vals',
]

struct_matrix._fields_ = [
    ('rows', c_int),
    ('cols', c_int),
    ('vals', POINTER(POINTER(c_float))),
]


class struct_data(Structure):
    pass

struct_data.__slots__ = [
    'w',
    'h',
    'X',
    'y',
    'shallow',
    'num_boxes',
    'boxes',
]

struct_data._fields_ = [
    ('w', c_int),
    ('h', c_int),
    ('X', struct_matrix),
    ('y', struct_matrix),
    ('shallow', c_int),
    ('num_boxes', POINTER(c_int)),
    ('boxes', POINTER(POINTER(struct_box))),
]


class struct_load_args(Structure):
    pass

struct_load_args.__slots__ = [
    'threads',
    'paths',
    'path',
    'n',
    'm',
    'labels',
    'h',
    'w',
    'out_w',
    'out_h',
    'nh',
    'nw',
    'num_boxes',
    'min',
    'max',
    'size',
    'classes',
    'background',
    'scale',
    'center',
    'coords',
    'jitter',
    'angle',
    'aspect',
    'saturation',
    'exposure',
    'hue',
    'd',
    'im',
    'resized',
    'type',
    'hierarchy',
]

struct_load_args._fields_ = [
    ('threads', c_int),
    ('paths', POINTER(c_char_p)),
    ('path', String),
    ('n', c_int),
    ('m', c_int),
    ('labels', POINTER(c_char_p)),
    ('h', c_int),
    ('w', c_int),
    ('out_w', c_int),
    ('out_h', c_int),
    ('nh', c_int),
    ('nw', c_int),
    ('num_boxes', c_int),
    ('min', c_int),
    ('max', c_int),
    ('size', c_int),
    ('classes', c_int),
    ('background', c_int),
    ('scale', c_int),
    ('center', c_int),
    ('coords', c_int),
    ('jitter', c_float),
    ('angle', c_float),
    ('aspect', c_float),
    ('saturation', c_float),
    ('exposure', c_float),
    ('hue', c_float),
    ('d', POINTER(struct_data)),
    ('im', POINTER(struct_image)),
    ('resized', POINTER(struct_image)),
    ('type', data_type),
    ('hierarchy', POINTER(struct_tree)),
]


class struct_box_label(Structure):
    pass

struct_box_label.__slots__ = [
    'id',
    'x',
    'y',
    'w',
    'h',
    'left',
    'right',
    'top',
    'bottom',
]

struct_box_label._fields_ = [
    ('id', c_int),
    ('x', c_float),
    ('y', c_float),
    ('w', c_float),
    ('h', c_float),
    ('left', c_float),
    ('right', c_float),
    ('top', c_float),
    ('bottom', c_float),
]


get_base_args = _darknet.get_base_args
get_base_args.argtypes = [POINTER(struct_network)]
get_base_args.restype = struct_load_args

free_data = _darknet.free_data
free_data.argtypes = [struct_data]
free_data.restype = None


class struct_node(Structure):
    pass
    
struct_node.__slots__ = [
    'val',
    'next',
    'prev',
]

struct_node._fields_ = [
    ('val', POINTER(None)),
    ('next', POINTER(struct_node)),
    ('prev', POINTER(struct_node)),
]


class struct_list(Structure):
    pass
    
struct_list.__slots__ = [
    'size',
    'front',
    'back',
]

struct_list._fields_ = [
    ('size', c_int),
    ('front', POINTER(struct_node)),
    ('back', POINTER(struct_node)),
]


load_data = _darknet.load_data
load_data.argtypes = [struct_load_args]
load_data.restype = c_ulong

read_data_cfg = _darknet.read_data_cfg
read_data_cfg.argtypes = [String]
read_data_cfg.restype = POINTER(struct_list)

read_cfg = _darknet.read_cfg
read_cfg.argtypes = [String]
read_cfg.restype = POINTER(struct_list)

read_file = _darknet.read_file
read_file.argtypes = [String]
read_file.restype = POINTER(c_ubyte)

resize_data = _darknet.resize_data
resize_data.argtypes = [struct_data, c_int, c_int]
resize_data.restype = struct_data

tile_data = _darknet.tile_data
tile_data.argtypes = [struct_data, c_int, c_int]
tile_data.restype = POINTER(struct_data)

select_data = _darknet.select_data
select_data.argtypes = [POINTER(struct_data), POINTER(c_int)]
select_data.restype = struct_data

forward_network = _darknet.forward_network
forward_network.argtypes = [POINTER(struct_network)]
forward_network.restype = None

backward_network = _darknet.backward_network
backward_network.argtypes = [POINTER(struct_network)]
backward_network.restype = None

update_network = _darknet.update_network
update_network.argtypes = [POINTER(struct_network)]
update_network.restype = None

dot_cpu = _darknet.dot_cpu
dot_cpu.argtypes = [c_int, POINTER(c_float), c_int, POINTER(c_float), c_int]
dot_cpu.restype = c_float

axpy_cpu = _darknet.axpy_cpu
axpy_cpu.argtypes = [c_int, c_float, POINTER(c_float), c_int, POINTER(c_float), c_int]
axpy_cpu.restype = None

copy_cpu = _darknet.copy_cpu
copy_cpu.argtypes = [c_int, POINTER(c_float), c_int, POINTER(c_float), c_int]
copy_cpu.restype = None

scal_cpu = _darknet.scal_cpu
scal_cpu.argtypes = [c_int, c_float, POINTER(c_float), c_int]
scal_cpu.restype = None

fill_cpu = _darknet.fill_cpu
fill_cpu.argtypes = [c_int, c_float, POINTER(c_float), c_int]
fill_cpu.restype = None

normalize_cpu = _darknet.normalize_cpu
normalize_cpu.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), c_int, c_int, c_int]
normalize_cpu.restype = None

softmax = _darknet.softmax
softmax.argtypes = [POINTER(c_float), c_int, c_float, c_int, POINTER(c_float)]
softmax.restype = None

best_3d_shift_r = _darknet.best_3d_shift_r
best_3d_shift_r.argtypes = [struct_image, struct_image, c_int, c_int]
best_3d_shift_r.restype = c_int

axpy_gpu = _darknet.axpy_gpu
axpy_gpu.argtypes = [c_int, c_float, POINTER(c_float), c_int, POINTER(c_float), c_int]
axpy_gpu.restype = None

fill_gpu = _darknet.fill_gpu
fill_gpu.argtypes = [c_int, c_float, POINTER(c_float), c_int]
fill_gpu.restype = None

scal_gpu = _darknet.scal_gpu
scal_gpu.argtypes = [c_int, c_float, POINTER(c_float), c_int]
scal_gpu.restype = None

copy_gpu = _darknet.copy_gpu
copy_gpu.argtypes = [c_int, POINTER(c_float), c_int, POINTER(c_float), c_int]
copy_gpu.restype = None

cuda_set_device = _darknet.cuda_set_device
cuda_set_device.argtypes = [c_int]
cuda_set_device.restype = None

cuda_free = _darknet.cuda_free
cuda_free.argtypes = [POINTER(c_float)]
cuda_free.restype = None

cuda_make_array = _darknet.cuda_make_array
cuda_make_array.argtypes = [POINTER(c_float), c_size_t]
cuda_make_array.restype = POINTER(c_float)

cuda_pull_array = _darknet.cuda_pull_array
cuda_pull_array.argtypes = [POINTER(c_float), POINTER(c_float), c_size_t]
cuda_pull_array.restype = None

cuda_mag_array = _darknet.cuda_mag_array
cuda_mag_array.argtypes = [POINTER(c_float), c_size_t]
cuda_mag_array.restype = c_float

cuda_push_array = _darknet.cuda_push_array
cuda_push_array.argtypes = [POINTER(c_float), POINTER(c_float), c_size_t]
cuda_push_array.restype = None

forward_network_gpu = _darknet.forward_network_gpu
forward_network_gpu.argtypes = [POINTER(struct_network)]
forward_network_gpu.restype = None

backward_network_gpu = _darknet.backward_network_gpu
backward_network_gpu.argtypes = [POINTER(struct_network)]
backward_network_gpu.restype = None

update_network_gpu = _darknet.update_network_gpu
update_network_gpu.argtypes = [POINTER(struct_network)]
update_network_gpu.restype = None

train_networks = _darknet.train_networks
train_networks.argtypes = [POINTER(POINTER(struct_network)), c_int, struct_data, c_int]
train_networks.restype = c_float

sync_nets = _darknet.sync_nets
sync_nets.argtypes = [POINTER(POINTER(struct_network)), c_int, c_int]
sync_nets.restype = None

harmless_update_network_gpu = _darknet.harmless_update_network_gpu
harmless_update_network_gpu.argtypes = [POINTER(struct_network)]
harmless_update_network_gpu.restype = None

get_label = _darknet.get_label
get_label.argtypes = [POINTER(POINTER(struct_image)), String, c_int]
get_label.restype = struct_image

draw_label = _darknet.draw_label
draw_label.argtypes = [struct_image, c_int, c_int, struct_image, POINTER(c_float)]
draw_label.restype = None

save_image = _darknet.save_image
save_image.argtypes = [struct_image, String]
save_image.restype = None

save_image_options = _darknet.save_image_options
save_image_options.argtypes = [struct_image, String, IMTYPE, c_int]
save_image_options.restype = None

get_next_batch = _darknet.get_next_batch
get_next_batch.argtypes = [struct_data, c_int, c_int, POINTER(c_float), POINTER(c_float)]
get_next_batch.restype = None

grayscale_image_3c = _darknet.grayscale_image_3c
grayscale_image_3c.argtypes = [struct_image]
grayscale_image_3c.restype = None

normalize_image = _darknet.normalize_image
normalize_image.argtypes = [struct_image]
normalize_image.restype = None

matrix_to_csv = _darknet.matrix_to_csv
matrix_to_csv.argtypes = [struct_matrix]
matrix_to_csv.restype = None

train_network_sgd = _darknet.train_network_sgd
train_network_sgd.argtypes = [POINTER(struct_network), struct_data, c_int]
train_network_sgd.restype = c_float

rgbgr_image = _darknet.rgbgr_image
rgbgr_image.argtypes = [struct_image]
rgbgr_image.restype = None

copy_data = _darknet.copy_data
copy_data.argtypes = [struct_data]
copy_data.restype = struct_data

concat_data = _darknet.concat_data
concat_data.argtypes = [struct_data, struct_data]
concat_data.restype = struct_data

load_cifar10_data = _darknet.load_cifar10_data
load_cifar10_data.argtypes = [String]
load_cifar10_data.restype = struct_data

matrix_topk_accuracy = _darknet.matrix_topk_accuracy
matrix_topk_accuracy.argtypes = [struct_matrix, struct_matrix, c_int]
matrix_topk_accuracy.restype = c_float

matrix_add_matrix = _darknet.matrix_add_matrix
matrix_add_matrix.argtypes = [struct_matrix, struct_matrix]
matrix_add_matrix.restype = None

scale_matrix = _darknet.scale_matrix
scale_matrix.argtypes = [struct_matrix, c_float]
scale_matrix.restype = None

csv_to_matrix = _darknet.csv_to_matrix
csv_to_matrix.argtypes = [String]
csv_to_matrix.restype = struct_matrix

network_accuracies = _darknet.network_accuracies
network_accuracies.argtypes = [POINTER(struct_network), struct_data, c_int]
network_accuracies.restype = POINTER(c_float)

train_network_datum = _darknet.train_network_datum
train_network_datum.argtypes = [POINTER(struct_network)]
train_network_datum.restype = c_float

make_random_image = _darknet.make_random_image
make_random_image.argtypes = [c_int, c_int, c_int]
make_random_image.restype = struct_image

denormalize_connected_layer = _darknet.denormalize_connected_layer
denormalize_connected_layer.argtypes = [struct_layer]
denormalize_connected_layer.restype = None

denormalize_convolutional_layer = _darknet.denormalize_convolutional_layer
denormalize_convolutional_layer.argtypes = [struct_layer]
denormalize_convolutional_layer.restype = None

statistics_connected_layer = _darknet.statistics_connected_layer
statistics_connected_layer.argtypes = [struct_layer]
statistics_connected_layer.restype = None

rescale_weights = _darknet.rescale_weights
rescale_weights.argtypes = [struct_layer, c_float, c_float]
rescale_weights.restype = None

rgbgr_weights = _darknet.rgbgr_weights
rgbgr_weights.argtypes = [struct_layer]
rgbgr_weights.restype = None

get_weights = _darknet.get_weights
get_weights.argtypes = [struct_layer]
get_weights.restype = POINTER(struct_image)

get_detection_detections = _darknet.get_detection_detections
get_detection_detections.argtypes = [struct_layer, c_int, c_int, c_float, POINTER(struct_detection)]
get_detection_detections.restype = None

option_find_str = _darknet.option_find_str
option_find_str.argtypes = [POINTER(struct_list), String, String]
if sizeof(c_int) == sizeof(c_void_p):
    option_find_str.restype = ReturnString
else:
    option_find_str.restype = String
    option_find_str.errcheck = ReturnString

option_find_int = _darknet.option_find_int
option_find_int.argtypes = [POINTER(struct_list), String, c_int]
option_find_int.restype = c_int

option_find_int_quiet = _darknet.option_find_int_quiet
option_find_int_quiet.argtypes = [POINTER(struct_list), String, c_int]
option_find_int_quiet.restype = c_int

parse_network_cfg = _darknet.parse_network_cfg
parse_network_cfg.argtypes = [String]
parse_network_cfg.restype = POINTER(struct_network)

save_weights = _darknet.save_weights
save_weights.argtypes = [POINTER(struct_network), String]
save_weights.restype = None

load_weights = _darknet.load_weights
load_weights.argtypes = [POINTER(struct_network), String]
load_weights.restype = None

save_weights_upto = _darknet.save_weights_upto
save_weights_upto.argtypes = [POINTER(struct_network), String, c_int]
save_weights_upto.restype = None

load_weights_upto = _darknet.load_weights_upto
load_weights_upto.argtypes = [POINTER(struct_network), String, c_int, c_int]
load_weights_upto.restype = None

zero_objectness = _darknet.zero_objectness
zero_objectness.argtypes = [struct_layer]
zero_objectness.restype = None

get_region_detections = _darknet.get_region_detections
get_region_detections.argtypes = [struct_layer, c_int, c_int, c_int, c_int, c_float, POINTER(c_int), c_float, c_int, POINTER(struct_detection)]
get_region_detections.restype = None

get_yolo_detections = _darknet.get_yolo_detections
get_yolo_detections.argtypes = [struct_layer, c_int, c_int, c_int, c_int, c_float, POINTER(c_int), c_int, POINTER(struct_detection)]
get_yolo_detections.restype = c_int

free_network = _darknet.free_network
free_network.argtypes = [POINTER(struct_network)]
free_network.restype = None

set_batch_network = _darknet.set_batch_network
set_batch_network.argtypes = [POINTER(struct_network), c_int]
set_batch_network.restype = None

set_temp_network = _darknet.set_temp_network
set_temp_network.argtypes = [POINTER(struct_network), c_float]
set_temp_network.restype = None

load_image = _darknet.load_image
load_image.argtypes = [String, c_int, c_int, c_int]
load_image.restype = struct_image

load_image_color = _darknet.load_image_color
load_image_color.argtypes = [String, c_int, c_int]
load_image_color.restype = struct_image

make_image = _darknet.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = struct_image

resize_image = _darknet.resize_image
resize_image.argtypes = [struct_image, c_int, c_int]
resize_image.restype = struct_image

censor_image = _darknet.censor_image
censor_image.argtypes = [struct_image, c_int, c_int, c_int, c_int]
censor_image.restype = None

letterbox_image = _darknet.letterbox_image
letterbox_image.argtypes = [struct_image, c_int, c_int]
letterbox_image.restype = struct_image

crop_image = _darknet.crop_image
crop_image.argtypes = [struct_image, c_int, c_int, c_int, c_int]
crop_image.restype = struct_image

center_crop_image = _darknet.center_crop_image
center_crop_image.argtypes = [struct_image, c_int, c_int]
center_crop_image.restype = struct_image

resize_min = _darknet.resize_min
resize_min.argtypes = [struct_image, c_int]
resize_min.restype = struct_image

resize_max = _darknet.resize_max
resize_max.argtypes = [struct_image, c_int]
resize_max.restype = struct_image

threshold_image = _darknet.threshold_image
threshold_image.argtypes = [struct_image, c_float]
threshold_image.restype = struct_image

mask_to_rgb = _darknet.mask_to_rgb
mask_to_rgb.argtypes = [struct_image]
mask_to_rgb.restype = struct_image

resize_network = _darknet.resize_network
resize_network.argtypes = [POINTER(struct_network), c_int, c_int]
resize_network.restype = c_int

free_matrix = _darknet.free_matrix
free_matrix.argtypes = [struct_matrix]
free_matrix.restype = None

test_resize = _darknet.test_resize
test_resize.argtypes = [String]
test_resize.restype = None

show_image = _darknet.show_image
show_image.argtypes = [struct_image, String, c_int]
show_image.restype = c_int

copy_image = _darknet.copy_image
copy_image.argtypes = [struct_image]
copy_image.restype = struct_image

draw_box_width = _darknet.draw_box_width
draw_box_width.argtypes = [struct_image, c_int, c_int, c_int, c_int, c_int, c_float, c_float, c_float]
draw_box_width.restype = None

get_current_rate = _darknet.get_current_rate
get_current_rate.argtypes = [POINTER(struct_network)]
get_current_rate.restype = c_float

composite_3d = _darknet.composite_3d
composite_3d.argtypes = [String, String, String, c_int]
composite_3d.restype = None

load_data_old = _darknet.load_data_old
load_data_old.argtypes = [POINTER(c_char_p), c_int, c_int, POINTER(c_char_p), c_int, c_int, c_int]
load_data_old.restype = struct_data

get_current_batch = _darknet.get_current_batch
get_current_batch.argtypes = [POINTER(struct_network)]
get_current_batch.restype = c_size_t

constrain_image = _darknet.constrain_image
constrain_image.argtypes = [struct_image]
constrain_image.restype = None

get_network_image_layer = _darknet.get_network_image_layer
get_network_image_layer.argtypes = [POINTER(struct_network), c_int]
get_network_image_layer.restype = struct_image

get_network_output_layer = _darknet.get_network_output_layer
get_network_output_layer.argtypes = [POINTER(struct_network)]
get_network_output_layer.restype = struct_layer

top_predictions = _darknet.top_predictions
top_predictions.argtypes = [POINTER(struct_network), c_int, POINTER(c_int)]
top_predictions.restype = None

flip_image = _darknet.flip_image
flip_image.argtypes = [struct_image]
flip_image.restype = None

ghost_image = _darknet.ghost_image
ghost_image.argtypes = [struct_image, struct_image, c_int, c_int]
ghost_image.restype = None

network_accuracy = _darknet.network_accuracy
network_accuracy.argtypes = [POINTER(struct_network), struct_data]
network_accuracy.restype = c_float

random_distort_image = _darknet.random_distort_image
random_distort_image.argtypes = [struct_image, c_float, c_float, c_float]
random_distort_image.restype = None

fill_image = _darknet.fill_image
fill_image.argtypes = [struct_image, c_float]
fill_image.restype = None

grayscale_image = _darknet.grayscale_image
grayscale_image.argtypes = [struct_image]
grayscale_image.restype = struct_image

rotate_image_cw = _darknet.rotate_image_cw
rotate_image_cw.argtypes = [struct_image, c_int]
rotate_image_cw.restype = None

what_time_is_it_now = _darknet.what_time_is_it_now
what_time_is_it_now.argtypes = []
what_time_is_it_now.restype = c_double

rotate_image = _darknet.rotate_image
rotate_image.argtypes = [struct_image, c_float]
rotate_image.restype = struct_image

visualize_network = _darknet.visualize_network
visualize_network.argtypes = [POINTER(struct_network)]
visualize_network.restype = None

box_iou = _darknet.box_iou
box_iou.argtypes = [struct_box, struct_box]
box_iou.restype = c_float

load_all_cifar10 = _darknet.load_all_cifar10
load_all_cifar10.argtypes = []
load_all_cifar10.restype = struct_data

read_boxes = _darknet.read_boxes
read_boxes.argtypes = [String, POINTER(c_int)]
read_boxes.restype = POINTER(struct_box_label)

float_to_box = _darknet.float_to_box
float_to_box.argtypes = [POINTER(c_float), c_int]
float_to_box.restype = struct_box

draw_detections = _darknet.draw_detections
draw_detections.argtypes = [struct_image, POINTER(struct_detection), c_int, c_float, POINTER(c_char_p), POINTER(POINTER(struct_image)), c_int]
draw_detections.restype = None

network_predict_data = _darknet.network_predict_data
network_predict_data.argtypes = [POINTER(struct_network), struct_data]
network_predict_data.restype = struct_matrix

load_alphabet = _darknet.load_alphabet
load_alphabet.argtypes = []
load_alphabet.restype = POINTER(POINTER(struct_image))

get_network_image = _darknet.get_network_image
get_network_image.argtypes = [POINTER(struct_network)]
get_network_image.restype = struct_image

network_predict = _darknet.network_predict
network_predict.argtypes = [POINTER(struct_network), POINTER(c_float)]
network_predict.restype = POINTER(c_float)

network_width = _darknet.network_width
network_width.argtypes = [POINTER(struct_network)]
network_width.restype = c_int

network_height = _darknet.network_height
network_height.argtypes = [POINTER(struct_network)]
network_height.restype = c_int

network_predict_image = _darknet.network_predict_image
network_predict_image.argtypes = [POINTER(struct_network), struct_image]
network_predict_image.restype = POINTER(c_float)

get_network_boxes = _darknet.get_network_boxes
get_network_boxes.argtypes = [POINTER(struct_network), c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(struct_detection)

free_detections = _darknet.free_detections
free_detections.argtypes = [POINTER(struct_detection), c_int]
free_detections.restype = None

reset_network_state = _darknet.reset_network_state
reset_network_state.argtypes = [POINTER(struct_network), c_int]
reset_network_state.restype = None

get_labels = _darknet.get_labels
get_labels.argtypes = [String]
get_labels.restype = POINTER(c_char_p)

do_nms_obj = _darknet.do_nms_obj
do_nms_obj.argtypes = [POINTER(struct_detection), c_int, c_int, c_float]
do_nms_obj.restype = None

do_nms_sort = _darknet.do_nms_sort
do_nms_sort.argtypes = [POINTER(struct_detection), c_int, c_int, c_float]
do_nms_sort.restype = None

make_matrix = _darknet.make_matrix
make_matrix.argtypes = [c_int, c_int]
make_matrix.restype = struct_matrix

open_video_stream = _darknet.open_video_stream
open_video_stream.argtypes = [String, c_int, c_int, c_int, c_int]
open_video_stream.restype = POINTER(None)

get_image_from_stream = _darknet.get_image_from_stream
get_image_from_stream.argtypes = [POINTER(None)]
get_image_from_stream.restype = struct_image

make_window = _darknet.make_window
make_window.argtypes = [String, c_int, c_int, c_int]
make_window.restype = None

free_image = _darknet.free_image
free_image.argtypes = [struct_image]
free_image.restype = None

train_network = _darknet.train_network
train_network.argtypes = [POINTER(struct_network), struct_data]
train_network.restype = c_float

load_data_in_thread = _darknet.load_data_in_thread
load_data_in_thread.argtypes = [struct_load_args]
load_data_in_thread.restype = c_ulong

load_data_blocking = _darknet.load_data_blocking
load_data_blocking.argtypes = [struct_load_args]
load_data_blocking.restype = None

get_paths = _darknet.get_paths
get_paths.argtypes = [String]
get_paths.restype = POINTER(struct_list)

hierarchy_predictions = _darknet.hierarchy_predictions
hierarchy_predictions.argtypes = [POINTER(c_float), c_int, POINTER(struct_tree), c_int, c_int]
hierarchy_predictions.restype = None

change_leaves = _darknet.change_leaves
change_leaves.argtypes = [POINTER(struct_tree), String]
change_leaves.restype = None

find_int_arg = _darknet.find_int_arg
find_int_arg.argtypes = [c_int, POINTER(c_char_p), String, c_int]
find_int_arg.restype = c_int

find_float_arg = _darknet.find_float_arg
find_float_arg.argtypes = [c_int, POINTER(c_char_p), String, c_float]
find_float_arg.restype = c_float

find_arg = _darknet.find_arg
find_arg.argtypes = [c_int, POINTER(c_char_p), String]
find_arg.restype = c_int

find_char_arg = _darknet.find_char_arg
find_char_arg.argtypes = [c_int, POINTER(c_char_p), String, String]
if sizeof(c_int) == sizeof(c_void_p):
    find_char_arg.restype = ReturnString
else:
    find_char_arg.restype = String
    find_char_arg.errcheck = ReturnString

basecfg = _darknet.basecfg
basecfg.argtypes = [String]
if sizeof(c_int) == sizeof(c_void_p):
    basecfg.restype = ReturnString
else:
    basecfg.restype = String
    basecfg.errcheck = ReturnString

find_replace = _darknet.find_replace
find_replace.argtypes = [String, String, String, String]
find_replace.restype = None

free_ptrs = _darknet.free_ptrs
free_ptrs.argtypes = [POINTER(POINTER(None)), c_int]
free_ptrs.restype = None

"""
fgetl = _darknet.fgetl
fgetl.argtypes = [POINTER(FILE)]
if sizeof(c_int) == sizeof(c_void_p):
    fgetl.restype = ReturnString
else:
    fgetl.restype = String
    fgetl.errcheck = ReturnString
"""

strip = _darknet.strip
strip.argtypes = [String]
strip.restype = None

sec = _darknet.sec
sec.argtypes = [c_long]
sec.restype = c_float

list_to_array = _darknet.list_to_array
list_to_array.argtypes = [POINTER(struct_list)]
list_to_array.restype = POINTER(POINTER(None))

top_k = _darknet.top_k
top_k.argtypes = [POINTER(c_float), c_int, c_int, POINTER(c_int)]
top_k.restype = None

read_map = _darknet.read_map
read_map.argtypes = [String]
read_map.restype = POINTER(c_int)

error = _darknet.error
error.argtypes = [String]
error.restype = None

max_index = _darknet.max_index
max_index.argtypes = [POINTER(c_float), c_int]
max_index.restype = c_int

max_int_index = _darknet.max_int_index
max_int_index.argtypes = [POINTER(c_int), c_int]
max_int_index.restype = c_int

sample_array = _darknet.sample_array
sample_array.argtypes = [POINTER(c_float), c_int]
sample_array.restype = c_int

random_index_order = _darknet.random_index_order
random_index_order.argtypes = [c_int, c_int]
random_index_order.restype = POINTER(c_int)

free_list = _darknet.free_list
free_list.argtypes = [POINTER(struct_list)]
free_list.restype = None

mse_array = _darknet.mse_array
mse_array.argtypes = [POINTER(c_float), c_int]
mse_array.restype = c_float

variance_array = _darknet.variance_array
variance_array.argtypes = [POINTER(c_float), c_int]
variance_array.restype = c_float

mag_array = _darknet.mag_array
mag_array.argtypes = [POINTER(c_float), c_int]
mag_array.restype = c_float

scale_array = _darknet.scale_array
scale_array.argtypes = [POINTER(c_float), c_int, c_float]
scale_array.restype = None

mean_array = _darknet.mean_array
mean_array.argtypes = [POINTER(c_float), c_int]
mean_array.restype = c_float

sum_array = _darknet.sum_array
sum_array.argtypes = [POINTER(c_float), c_int]
sum_array.restype = c_float

normalize_array = _darknet.normalize_array
normalize_array.argtypes = [POINTER(c_float), c_int]
normalize_array.restype = None

read_intlist = _darknet.read_intlist
read_intlist.argtypes = [String, POINTER(c_int), c_int]
read_intlist.restype = POINTER(c_int)

rand_size_t = _darknet.rand_size_t
rand_size_t.argtypes = []
rand_size_t.restype = c_size_t

rand_normal = _darknet.rand_normal
rand_normal.argtypes = []
rand_normal.restype = c_float

rand_uniform = _darknet.rand_uniform
rand_uniform.argtypes = [c_float, c_float]
rand_uniform.restype = c_float
