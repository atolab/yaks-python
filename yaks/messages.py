# Copyright (c) 2018 ADLINK Technology Inc.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - Yaks API


'''
This code uses
https://docs.python.org/3.6/library/struct.html
for pack and unpack of the network messages

MESSAGE FORMAT:
LITTLE ENDIAN



7 6 5 4 3 2 1 0
+-+-+-+-+-+-+-+-+ ----------------------+
|  MESSAGE CODE |    8bit               |
+-+-+-+-+-+-+-+-+                       |
|X|X|X|X|X|A|S|P|    8bit               +--> Header
+-+-+-+-+-+-+-+-+                       |
~   Coor. ID    ~  VLE max 64bit        |
+---------------+                       |
~   Properties  ~ --> Present if P = 1  |
+---------------+ ----------------------+
~     Body      ~ --> its structure depends on the message code
+---------------+


WIRE MESSAGE:

 7 6 5 4 3 2 1 0
+-+-+-+-+-+-+-+-+
~    Lenght     ~ VLE max 64bit
+-+-+-+-+-+-+-+-+ ----------------------+
|  MESSAGE CODE |    8bit               |
+-+-+-+-+-+-+-+-+                       |
|X|X|X|X|X|A|S|P|    8bit               +--> Header
+-+-+-+-+-+-+-+-+                       |
~    Corr. id   ~  VLE max 64bit        |
+---------------+                       |
~   Properties  ~ --> Present if P = 1  |
+---------------+ ----------------------+
~     Body      ~ VL
+---------------+


'''
import random
import struct
import json
import hexdump
from enum import Enum
from yaks.encoder import VLEEncoder
from yaks.value import Value
from yaks.path import Path
from yaks.selector import Selector
from yaks.encoding import *
# Message Codes
OPEN = 0x01
CREATE = 0x02
DELETE = 0x03
PUT = 0xA0
PATCH = 0xA1
GET = 0xA2
SUB = 0xB0
UNSUB = 0xB1
NOTIFY = 0xB2
EVAL = 0xB3
OK = 0xD0
VALUES = 0xD1
ERROR = 0xE0


class EntityType(Enum):
    WORKSPACE = 0
    STORAGE = 1


class Message(object):

    def __init__(self, raw_message=None):
        self.encoder = VLEEncoder()
        self.raw_msg = raw_message
        self.message_code = 0x0
        # 8bit
        self.flags = 0x0
        # 8bit comprises A,S,P
        self.flag_a = 0x0
        # 1bit
        self.flag_s = 0x0
        # 1bit
        self.flag_p = 0x0
        # 1bit
        self.corr_id = 0x0
        # VLE max 64bit
        self.length = 0x0
        # 64bit
        self.properties = []

        # key-value tuple list (string,string)
        self.data = b''
        if self.raw_msg is not None:
            self.unpack()
            self.length = len(self.raw_msg)

    def __read_vle_field(self, buf, base_p):
        vle_field = []
        data = buf[base_p]
        vle_field.append(data.to_bytes(1, byteorder='big'))
        while data & 0x80:
            base_p = base_p + 1
            data = buf[base_p]
            vle_field.append(data.to_bytes(1, byteorder='big'))
        return self.encoder.decode(vle_field), base_p + 1

    def pack(self):
        header = struct.pack('<BB', self.message_code, self.flags)
        for b in self.encoder.encode(self.corr_id):
            header = header + b

        msg = header
        if self.flag_p:
            num_p = len(self.properties)
            for b in self.encoder.encode(num_p):
                msg = msg + b
            for p in self.properties:
                k = p.get('key').encode()
                v = p.get('value').encode()
                len_k = len(k)
                len_v = len(v)

                for b in self.encoder.encode(len_k):
                    msg = msg + b

                fmt = '<{}s'.format(len_k)
                msg = msg + struct.pack(fmt, k)

                for b in self.encoder.encode(len_v):
                    msg = msg + b

                fmt = '<{}s'.format(len_v)
                msg = msg + struct.pack(fmt, v)

        msg = msg + self.data
        self.raw_msg = msg
        self.length = len(self.raw_msg)
        return self.raw_msg

    def pack_for_transport(self):
        self.pack()
        vle_length = b''
        for b in self.encoder.encode(self.length):
            vle_length = vle_length + b
        return vle_length + self.raw_msg

    def unpack(self):
        sub_header = self.raw_msg[0:2]

        msg = struct.unpack('<BB', sub_header)
        self.message_code = msg[0]
        self.flags = msg[1]

        self.flag_a = (self.flags & 0x04) >> 2
        self.flag_s = (self.flags & 0x02) >> 1
        self.flag_p = self.flags & 0x01
        base_p = 2

        self.corr_id, base_p = self.__read_vle_field(self.raw_msg, base_p)

        if self.flag_p:
            num_p, base_p = self.__read_vle_field(self.raw_msg, base_p)
            for i in range(0, num_p):
                key_length, base_p = \
                    self.__read_vle_field(self.raw_msg, base_p)
                key_raw = self.raw_msg[base_p:base_p + key_length]
                k = struct.unpack('<{}s'.format(key_length),
                                  key_raw)[0].decode()
                base_p = base_p + key_length

                value_length, base_p = \
                    self.__read_vle_field(self.raw_msg, base_p)
                value_raw = self.raw_msg[base_p:base_p + value_length]
                v = struct.unpack('<{}s'.format(value_length),
                                  value_raw)[0].decode()
                base_p = base_p + value_length
                self.properties.append({'key': k, 'value': v})

        self.set_data(self.raw_msg[base_p:])
        # if len(self.data) > 0 and self.message_code in [VALUES]:
        #     self.encoding = self.__read_encoding(self.data, 0)
        return self

    def __add_vle(self, number):
        body = b''
        for b in self.encoder.encode(number):
            body = body + b
        return body

    def __get_vle(self, data, base_p):
        return self.__read_vle_field(data, base_p)

    def __add_string(self, value):
        body = b''
        len_p = len(value)
        for b in self.encoder.encode(len_p):
            body = body + b
        fmt = '<{}s'.format(len_p)
        body = body + struct.pack(fmt, value.encode())
        return body

    def __get_string(self, data, base_p):
        path_length, base_p = self.__read_vle_field(data, base_p)
        path_raw = data[base_p:base_p + path_length]
        string = struct.unpack('<{}s'.format(path_length),
                               path_raw)[0].decode()
        return string, base_p + path_length

    def __encode_list(self, value_list):
        data = b''
        llen = len(value_list)
        for b in self.encoder.encode(llen):
            data = data + b
        for e in value_list:
            e_len = len(e)
            for b in self.encoder.encode(e_len):
                data = data + b
            fmt = '<{}s'.format(e_len)
            data = data + struct.pack(fmt, e.encode())
        return data

    def __decode_list(self, data, base_p):
        value_list = []
        llen, base_p = self.__read_vle_field(data, base_p)
        for i in range(0, llen):
            s_len, base_p = self.__read_vle_field(data, base_p)
            s_raw = data[base_p: base_p + s_len]
            fmt = '<{}s'.format(s_len)
            value_list.append(struct.unpack(fmt, s_raw)[0].decode())
            base_p = base_p + s_len
        return value_list, base_p

    def __value_encoding(self, value):
        data = b''
        encoding = value.get_encoding()
        if encoding in [RAW, JSON, STRING]:
            len_v = len(value.get_value())
            data = data + struct.pack('<B', encoding)
            for b in self.encoder.encode(len_v):
                data = data + b
            fmt = '<{}s'.format(len_v)
            data = data + struct.pack(fmt, value.get_value().encode())
        elif encoding == SQL:
            data = data + struct.pack('<B', encoding)
            row_values, column_names = value.get_value()
            data = data + self.__encode_list(row_values)
            data = data + self.__encode_list(column_names)
        elif encoding == PROTOBUF:
            raise NotImplementedError('Not yet implemented')
        elif encoding == INVALID:
            raise ValueError('Encoding invalid')
        else:
            raise ValueError('Unknown encoding')
        return data

    def __value_decoding(self, data, base_p):
        v = None
        encoding = struct.unpack('<B', data[base_p: base_p + 1])[0]
        base_p = base_p + 1
        if encoding in [RAW, JSON, STRING]:
            len_v, base_p = self.__read_vle_field(data, base_p)
            fmt = '<{}s'.format(len_v)
            val_raw = data[base_p:base_p + len_v]
            v = struct.unpack(fmt, val_raw)[0].decode()
            base_p = base_p + len_v
        elif encoding == SQL:
            l_values, base_p = self.__decode_list(data, base_p)
            l_names, base_p = self.__decode_list(data, base_p)
            v = (l_values, l_names)
        elif encoding == PROTOBUF:
            raise NotImplementedError('Not yet implemented')
        elif encoding == INVALID:
            raise ValueError('Encoding invalid')
        else:
            raise ValueError('Unknown encoding')
        return Value(v, encoding), base_p

    def __add_key_value_list(self, kvs):
        body = b''
        num_p = len(kvs)
        for b in self.encoder.encode(num_p):
            body = body + b
        for p in kvs:
            k = p.get('key').to_string().encode()
            v = p.get('value')
            len_k = len(k)

            for b in self.encoder.encode(len_k):
                body = body + b

            fmt = '<{}s'.format(len_k)
            body = body + struct.pack(fmt, k)

            body = body + self.__value_encoding(v)
        return body

    def __get_key_value_list(self, data, base_p):
        kvs = []
        num_kvs, base_p = self.__read_vle_field(data, base_p)
        for i in range(0, num_kvs):
            key_length, base_p = self.__read_vle_field(data, base_p)
            key_raw = data[base_p:base_p + key_length]
            k = struct.unpack('<{}s'.format(key_length),
                              key_raw)[0].decode()
            base_p = base_p + key_length

            v, base_p = self.__value_decoding(data, base_p)
            kvs.append({'key': Path(k), 'value': v})
        return kvs, base_p

    def add_path(self, path):
        self.data = self.__add_string(path.to_string())

    def get_path(self):
        p, _ = self.__get_string(self.data, 0)
        return Path(p)

    def add_selector(self, selector):
        self.data = self.__add_string(selector.to_string())

    def get_selector(self):
        s, _ = self.__get_string(self.data, 0)
        return Selector(s)

    def add_notification(self, subid, kvs):
        self.data = self.__add_string(subid) + self.__add_key_value_list(kvs)

    def get_notification(self):
        subid, pos = self.__get_string(self.data, 0)
        kvs, _ = self.__get_key_value_list(self.data, pos)
        return subid, kvs

    def add_subscription(self, selector):
        self.data = self.__add_string(selector.to_string())

    def add_subscription_id(self, subid):
        self.data = self.__add_string(subid)

    def get_subscription(self):
        subid, _ = self.__get_string(self.data, 0)
        return Selector(subid)

    def get_subscription_id(self):
        subid, _ = self.__get_string(self.data, 0)
        return subid

    def add_values(self, kvs):
        self.data = self.__add_key_value_list(kvs)

    def get_values(self):
        kvs, _ = self.__get_key_value_list(self.data, 0)
        return kvs

    def add_error(self, error_code):
        self.data = self.__add_vle(error_code)

    def get_error(self):
        e, _ = self.__get_vle(self.data, 0)
        return e

    def set_p(self):
        self.flag_p = 1
        self.flags = self.flags | 0x01

    def unset_p(self):
        self.flag_p = 0
        self.flags = self.flags ^ 0x01

    def set_s(self):
        self.flag_s = 1
        self.flags = self.flags | 0x02

    def unset_s(self):
        self.flag_s = 0
        self.flags = self.flags ^ 0x02

    def set_a(self):
        self.flag_a = 1
        self.flags = self.flags | 0x04

    def unset_a(self):
        self.flag_a = 0
        self.flags = self.flags ^ 0x04

    def set_data(self, data):
        self.data = data

    def remove_data(self):
        self.data = b''

    def get_property(self, key):
        f = [x for x in self.properties if x.get('key') == key]
        if len(f) > 0:
            return f[0].get('value')
        return None

    def add_property(self, key, value):
        self.set_p()
        self.properties.append({'key': key, 'value': value})

    def remove_property(self, key):
        f = [x for x in self.properties if x.get('key') == key]
        if len(f) > 0:
            self.properties.remove(f[0])
        if len(self.properties) == 0:
            self.unset_p()

    def dump(self):
        return hexdump.hexdump(self.raw_msg, result='return')

    def dump_net(self):
        return hexdump.hexdump(self.pack_for_transport(), result='return')

    def pprint(self):
        pretty = '\n############ YAKS FE SOCKET MESSAGE ###################' \
                 + '\n# CODE: {}'.format(self.message_code) \
                 + '\n# CORR.ID: {}'.format(self.corr_id) \
                 + '\n# LENGTH: {}'.format(self.length) \
                 + '\n# FLAGS: RAW: {} | A:{} S:{} P:{}'.\
                format(self.flags, self.flag_a, self.flag_s, self.flag_p)

        if self.flag_p:
            pretty = pretty + '\n# HAS PROPERTIES\n# NUMBER OF PROPERTIES:' \
                              ' {}'.format(len(self.properties))
            for p in self.properties:
                pretty = pretty + '\n#========\n# KEY:{} VALUE: {}'.\
                    format(p.get('key'), p.get('value'))
        pretty = pretty + '\n#========\nDATA: {}'.format(self.data)\
                 + '\n#######################################################'
        return pretty

    def generate_corr_id(self):
        self.corr_id = random.getrandbits(32)


class MessageOpen(Message):
    def __init__(self, username=None, password=None):
        super(MessageOpen, self).__init__()
        self.generate_corr_id()
        self.message_code = OPEN
        if username and password:
            self.add_property('yaks.login', '{}:{}'.format(username, password))


class MessageCreate(Message):
    def __init__(self, ctype, path, properties=None):
        super(MessageCreate, self).__init__()
        self.message_code = CREATE
        self.generate_corr_id()

        if properties is not None:
            for pname in properties:
                pvalue = properties.get(pname)
                if isinstance(pvalue, str):
                    self.add_property(pname, pvalue)
                elif isinstance(pvalue, int) or isinstance(pvalue, float):
                    self.add_property(pname, '{}'.format(pvalue))
                elif isinstance(pvalue, dict):
                    self.add_property(pname, json.dumps(pvalue))
        if ctype is EntityType.WORKSPACE:
            self.set_a()
            self.add_path(path)
        elif ctype is EntityType.STORAGE:
            self.set_s()
            self.add_selector(path)


class MessageDelete(Message):
    def __init__(self, id, dtype=None, path=None):
        super(MessageDelete, self).__init__()
        self.message_code = DELETE
        self.generate_corr_id()
        if dtype is EntityType.WORKSPACE:
            self.set_a()
            self.add_property('is.yaks.access.id', id)
        elif dtype is EntityType.STORAGE:
            self.set_s()
            self.add_property('is.yaks.storage.id', id)
        elif path is not None:
            self.add_property('is.yaks.access.id', id)
            self.add_path(path)


class MessagePut(Message):
    def __init__(self, aid, key, value):
        super(MessagePut, self).__init__()
        self.message_code = PUT
        self.generate_corr_id()
        self.add_property('is.yaks.access.id', aid)
        self.add_values([{'key': key,
                          'value': value}])


class MessagePatch(Message):
    def __init__(self, aid, key, value):
        super(MessagePatch, self).__init__()
        self.message_code = PATCH
        self.generate_corr_id()
        self.add_property('is.yaks.access.id', aid)
        self.add_values([{'key': key,
                          'value': value}])


class MessageGet(Message):
    def __init__(self, aid, key):
        super(MessageGet, self).__init__()
        self.message_code = GET
        self.generate_corr_id()
        self.add_property('is.yaks.access.id', aid)
        self.add_selector(key)


class MessageSub(Message):
    def __init__(self, aid, key):
        super(MessageSub, self).__init__()
        self.message_code = SUB
        self.generate_corr_id()
        self.add_property('is.yaks.access.id', aid)
        self.add_subscription(key)


class MessageUnsub(Message):
    def __init__(self, aid, subscription_id):
        super(MessageUnsub, self).__init__()
        self.message_code = UNSUB
        self.generate_corr_id()
        self.add_property('is.yaks.access.id', aid)
        self.add_subscription_id(subscription_id)


class MessageEval(Message):
    def __init__(self, aid, computation):
        super(MessageEval, self).__init__()
        self.message_code = EVAL
        self.generate_corr_id()
        self.add_property('is.yaks.access.id', aid)
        self.add_path(computation)


class MessageValues(Message):
    def __init__(self, cid, kvs):
        super(MessageValues, self).__init__()
        self.message_code = VALUES
        self.corr_id = cid
        self.add_values(kvs)


class MessageOk(Message):
    def __init__(self, corr_id):
        super(MessageOk, self).__init__()
        self.message_code = OK
        self.corr_id = corr_id
        # self.add_property('yaks.id', id)


class MessageError(Message):
    def __init__(self, corr_id, errno):
        super(MessageError, self).__init__()
        self.message_code = ERROR
        self.corr_id = corr_id
        # self.add_property('yaks.id', id)
        self.add_error(errno)
