import platform
import os
from ctypes import *


def get_lib_ext():
    system = platform.system()
    if system == 'Linux':
        return '.so'
    elif system == 'Darwin':
        return '.dylib'
    else:
        return '.dll'

def get_user_lib_path():
    system = platform.system()
    if system == 'Linux':
        return '/usr/local/lib'
    elif system == 'Darwin':
        return '/usr/local/lib'
    elif system in ['windows', 'Windows', 'win32']:
        return os.environ['ZENOH_HOME']
    else:
        return '/usr/local/lib'



system = platform.system()
if system in ['windows', 'Windows', 'win32']:
    zenoh_lib = 'zenohc' + get_lib_ext()
    zenoh_lib_path = get_user_lib_path() + os.sep + zenoh_lib    
else:
    zenoh_lib = 'libzenohc' + get_lib_ext()    
    zenoh_lib_path = get_user_lib_path() + os.sep + zenoh_lib


# typedef struct {
#   unsigned int r_pos;
#   unsigned int w_pos;
#   unsigned int capacity;
#   uint8_t* buf;
# } z_iobuf_t;

class z_iobuf_t(Structure):
    _fields_ = [('r_pos', c_uint),
                ('w_pos', c_uint),
                ('capacity', c_uint),
                ('buf', c_char_p)]

