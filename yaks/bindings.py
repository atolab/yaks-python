import platform
import os
from ctypes import *


Z_INT_RES_ID = 0
Z_STR_RES_ID = 1


Y_PUT       = 0x00
Y_UPDATE    = 0x01
Y_REMOVE    = 0x02


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


# typedef struct { enum result_kind tag; union { zenoh_t zenoh; int error; } value;} z_zenoh_result_t;


class z_res_id_t(Structure):
    _fields_ = [('rid', c_long),
                ('rname', c_char_p)]


class z_resource_id_t(Structure):
    _fields_ = [('kind', c_int),
                ('id', z_res_id_t)]


class z_data_info_t(Structure):
    _fields_ = [('flags', c_uint),
                ('encoding', c_ushort),
                ('kind', c_ushort)]


class z_iobuf_t(Structure):
    _fields_ = [('r_pos', c_uint),
                ('w_pos', c_uint),
                ('capacity', c_uint),
                ('buf', c_char_p)]

YAKS_SUBSCRIBER_CALLBACK_PROTO = CFUNCTYPE(None, z_resource_id_t, z_iobuf_t, z_data_info_t)
