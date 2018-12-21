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

import socket
import threading
import queue
import select
import os
from yaks.messages import *
from yaks.mvar import MVar
from yaks import path as ypath
from yaks.encoder import VLEEncoder
from yaks.logger import APILogger
from yaks.exceptions import ValidationError

BUFFSIZE = 1
ver = os.environ.get('YAKS_PYTHON_API_LOGFILE')
if ver is None:
    VERBOSE = False
else:
    VERBOSE = bool(os.environ.get('YAKS_PYTHON_API_VERBOSE'))
logger = APILogger(file_name=os.environ.get('YAKS_PYTHON_API_LOGFILE'),
                   debug_flag=VERBOSE)


class SendingThread(threading.Thread):
    def __init__(self, y):
        super(SendingThread, self).__init__()
        self.__yaks = y
        self.lock = self.__yaks.lock
        self.subscriptions = self.__yaks.subscriptions
        self.send_q = self.__yaks.send_queue
        self.sock = self.__yaks.sock
        self.waiting_msgs = self.__yaks.working_set
        self._is_running = False
        self.daemon = True

    def close(self):
        pass

    def send_error_to_all(self):
        for cid in list(self.waiting_msgs.keys()):
            _, var = self.waiting_msgs.get(cid)
            e_msg = MessageError(cid, 412)
            var.put(e_msg)
            self.waiting_msgs.pop(cid)

    def run(self):
        self._is_running = True
        while self._is_running and self.__yaks.is_connected:
            msg_s, var = self.send_q.get()
            logger.info('SendingThread', 'Message from queue')
            logger.debug('SendingThread', 'Message {}'.
                         format(msg_s.pprint()))
            self.lock.acquire()
            self.waiting_msgs.update({msg_s.corr_id: (msg_s, var)})
            try:
                self.sock.sendall(msg_s.pack_for_transport())
                logger.debug('SendingThread', 'Message Sent on Wire\n{}'.
                             format(msg_s.dump_net()))
            except ConnectionResetError as cre:
                logger.error('SendingThread',
                             'Server Closed connection {}'.format(cre))
                self.send_error_to_all()
                self.__yaks.is_connected = False
            except OSError as e:
                if e.errno == 9:
                    logger.error('SendingThread', 'Bad FD')
                self.send_error_to_all()
                self.__yaks.is_connected = False
            except struct.error as se:
                logger.error('SendingThread', 'Pack Error {}'.format(se))
                err = MessageError(msg_s.corr_id, 400)
                self.waiting_msgs.pop(msg_s.corr_id)
                var.put(err)
            finally:
                self.lock.release()


class ReceivingThread(threading.Thread):
    def __init__(self, y):
        super(ReceivingThread, self).__init__()
        self.__yaks = y
        self.lock = self.__yaks.lock
        self.sock = self.__yaks.sock
        self.send_q = self.__yaks.send_queue
        self.subscriptions = self.__yaks.subscriptions
        self.waiting_msgs = self.__yaks.working_set
        self._is_running = False
        self.daemon = True
        self.encoder = VLEEncoder()

    def close(self):
        self._is_running = False
        self.lock.acquire()
        self.sock.close()
        self.lock.release()

    def send_error_to_all(self):
        for cid in list(self.waiting_msgs.keys()):
            _, var = self.waiting_msgs.get(cid)
            e_msg = MessageError(cid, 412)
            var.put(e_msg)
            self.waiting_msgs.pop(cid)

    def read_length(self):
        l_vle = []
        data = self.sock.recv(BUFFSIZE)

        l_vle.append(data)
        while int.from_bytes(data, byteorder='big', signed=False) & 0x80:
            data = self.sock.recv(BUFFSIZE)
            l_vle.append(data)
        logger.info('ReceivingThread', 'Read VLE {} of {} bytes'.
                    format(l_vle, len(l_vle)))
        return self.encoder.decode(l_vle)

    def computation_wrapper(self, corrid, comp, p_a_s, path, params):
        if p_a_s:
            path = str(path)
        res = comp(path, **params)
        kvs = [{'key': Path(path), 'value': res}]
        v_msg = MessageValues(corrid, kvs)
        var = MVar()
        self.__yaks.send_queue.put((v_msg, var))

    def run(self):
        self._is_running = True
        while self._is_running and self.__yaks.is_connected:

            try:
                i, _, xs = select.select([self.sock], [], [self.sock])
            except OSError:
                self.lock.acquire()
                self.send_error_to_all()
                self.__yaks.is_connected = False
                self.lock.release()
            if len(xs) != 0:
                logger.error('ReceivingThread', 'Exception on socket')
            elif len(i) != 0:
                try:
                    logger.info('ReceivingThread', 'Socket ready')
                    self.lock.acquire()
                    length = self.read_length()
                    if length > 0:
                        data = b''
                        while len(data) < length:
                            data = data + self.sock.recv(BUFFSIZE)
                        msg_r = Message(data)
                        logger.info('ReceivingThread',
                                    'Read from socket {} bytes'.
                                    format(length))
                        logger.debug('ReceivingThread',
                                     'Message Received {} \n{}'.
                                     format(msg_r.pprint(), msg_r.dump()))
                        if msg_r.message_code == NOTIFY:
                            sid, kvs = msg_r.get_notification()
                            if sid in self.subscriptions:
                                cbk, p_a_s = self.subscriptions.get(sid)
                                if p_a_s:
                                    vs = []
                                    for kv in kvs:
                                        vs.append({
                                            'key': str(kv.get('key')),
                                            'value': kv.get('value')})
                                else:
                                    vs = kvs
                                threading.Thread(target=cbk, args=(vs,),
                                                 daemon=True).start()
                        if msg_r.message_code == GET:
                            selector = msg_r.get_selector()
                            args = selector.dict_from_properties()
                            for p in self.__yaks.evals:
                                if selector.is_prefixed_by_path(p.to_string()):
                                    c, p_a_s = self.__yaks.evals.get(p)
                                    threading.Thread(
                                        target=self.computation_wrapper,
                                        args=(
                                            msg_r.corr_id, c, p_a_s,
                                            selector.get_path(), args),
                                        daemon=True).start()
                        elif self.waiting_msgs.get(msg_r.corr_id) is None:
                            logger.info('ReceivingThread',
                                        'This message was not expected!')
                        else:
                            if msg_r.message_code == ERROR:
                                logger.info('ReceivingThread',
                                            'Got Error on Message {} '
                                            'Error Code: {}'
                                            .format(msg_r.corr_id,
                                                    msg_r.get_error()))
                            _, var = self.waiting_msgs.get(msg_r.corr_id)
                            self.waiting_msgs.pop(msg_r.corr_id)
                            var.put(msg_r)
                    else:
                        logger.error('ReceivingThread', 'Socket is closed!')
                        self.send_error_to_all()
                        self.sock.close()
                        self.sock.close()
                        self.__yaks.is_connected = False
                except struct.error as se:
                    logger.error('ReceivingThread',
                                 'Unpack Error {}'.format(se))
                except ConnectionResetError as cre:
                    logger.error('ReceivingThread',
                                 'Server Closed connection {}'.format(cre))
                    self.send_error_to_all()
                    self.__yaks.is_connected = False
                except OSError as e:
                    if e.errno == 9:
                        logger.error('ReceivingThread', 'Bad FD')
                    self.send_error_to_all()
                    self.__yaks.is_connected = False
                finally:
                    self.lock.release()
        if not self._is_running:
            self.close()


class Workspace(object):
    def __init__(self, y, id, path, properties):
        self.__yaks = y
        self.__subscriptions = self.__yaks.subscriptions
        self.__send_queue = self.__yaks.send_queue
        self.__evals = self.__yaks.evals
        self.id = id
        self.path = path
        self.properties = properties
        # self.encoding = encoding

    def put(self, path, value):
        if not isinstance(path, Path):
            path = Path(path)
        self.__yaks.check_connection()
        msg_put = MessagePut(self.id, path, value)
        var = MVar()
        self.__send_queue.put((msg_put, var))
        r = var.get()
        if YAKS.check_msg(r, msg_put.corr_id):
            return True
        return False

    def update(self, path, value):
        if not isinstance(path, Path):
            path = Path(path)
        self.__yaks.check_connection()
        msg_delta = MessagePatch(self.id, path, value)
        var = MVar()
        self.__send_queue.put((msg_delta, var))
        r = var.get()
        if YAKS.check_msg(r, msg_delta.corr_id):
            return True
        return False

    def remove(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        self.__yaks.check_connection()
        msg_rm = MessageDelete(self.id, path=path)
        var = MVar()
        self.__send_queue.put((msg_rm, var))
        r = var.get()
        if YAKS.check_msg(r, msg_rm.corr_id):
            if path in self.__evals:
                self.__evals.pop(path)
            return True
        return False

    def subscribe(self, selector, callback=None, paths_as_strings=True):
        if not isinstance(selector, Selector):
            selector = Selector(selector)
        msg_sub = MessageSub(self.id, selector)
        var = MVar()
        self.__send_queue.put((msg_sub, var))
        r = var.get()
        if YAKS.check_msg(r, msg_sub.corr_id):
            subid = r.get_property('is.yaks.subscription.id')
            if callback:
                self.__subscriptions.update(
                    {subid: (callback, paths_as_strings)})
            return subid
        raise \
            RuntimeError('subscribe {} failed with error code {}'.format(
                selector, r.get_error()))

    def get_subscriptions(self):
        self.__yaks.check_connection()
        return self.__subscriptions

    def unsubscribe(self, subscription_id):
        self.__yaks.check_connection()
        msg_unsub = MessageUnsub(self.id, subscription_id)
        var = MVar()
        self.__send_queue.put((msg_unsub, var))
        r = var.get()
        if YAKS.check_msg(r, msg_unsub.corr_id):
            self.__subscriptions.pop(subscription_id)
            return True
        return False

    def get(self, selector, paths_as_strings=True):
        if not isinstance(selector, Selector):
            selector = Selector(selector)
        self.__yaks.check_connection()
        msg_get = MessageGet(self.id, selector)
        var = MVar()
        self.__send_queue.put((msg_get, var))
        r = var.get()
        if YAKS.check_msg(r, msg_get.corr_id, expected=[VALUES]):
            kvs = r.get_values()
            if not paths_as_strings:
                return kvs
            vs = []
            for kv in kvs:
                vs.append({
                    'key': str(kv.get('key')),
                    'value': kv.get('value')})
            return vs
        raise \
         RuntimeError('get {} failed with error code {}'.format(
             selector, r.get_error()))

    def eval(self, path, computation, paths_as_strings=True):
        if not isinstance(path, Path):
            path = Path(path)
        self.__yaks.check_connection()
        msg_eval = MessageEval(self.id, path)
        var = MVar()
        self.__send_queue.put((msg_eval, var))
        r = var.get()
        if YAKS.check_msg(r, msg_eval.corr_id):
            self.__evals.update({path: (computation, paths_as_strings)})
            return True
        raise \
         RuntimeError('eval {} failed with error code {}'.format(
             path, r.get_error()))

    def dispose(self):
        self.__yaks.check_connection()
        var = MVar()
        msg = MessageDelete(self.id, EntityType.WORKSPACE)
        self.__send_queue.put((msg, var))
        r = var.get()
        if YAKS.check_msg(r, msg.corr_id):
            return True
        return False


class YAKS(object):
    def __init__(self):
        self.is_connected = False
        self.subscriptions = {}
        self.evals = {}
        self.send_queue = queue.Queue()
        self.address = None
        self.port = None
        self.accesses = {}
        self.storages = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.setblocking(1)
        self.lock = threading.Lock()
        self.working_set = {}
        self.is_connected = False
        self.st = None
        self.rt = None

    @classmethod
    def login(self, server_address, server_port=7887, properties={}):
        y = self()
        y.address = server_address
        y.port = server_port
        y.sock.connect((y.address, y.port))
        y.is_connected = True
        y.st = SendingThread(y)
        y.rt = ReceivingThread(y)
        y.st.start()
        y.rt.start()

        open_msg = MessageOpen()
        var = MVar()
        y.send_queue.put((open_msg, var))
        msg = var.get()
        if not YAKS.check_msg(msg, open_msg.corr_id):
            raise RuntimeError('Server response is wrong')
        return y

    @staticmethod
    def check_msg(msg, corr_id, expected=[OK]):
        return msg.message_code in expected and corr_id == msg.corr_id

    def check_connection(self):
        if not self.is_connected:
            raise ConnectionError('Lost connection with YAKS')
        pass

    def logout(self):
        self.st.close()
        self.rt.close()
        self.is_connected = False
        self.address = None
        self.port = None

    def workspace(self, path, properties=None):
        if not isinstance(path, Path):
            path = Path(path)
        create_msg = MessageCreate(EntityType.WORKSPACE, path)
        var = MVar()
        self.send_queue.put((create_msg, var))
        msg = var.get()
        if self.check_msg(msg, create_msg.corr_id):
            id = msg.get_property('is.yaks.access.id')
            acc = Workspace(self, id, path, properties)
            self.accesses.update({id: acc})
            return acc
        else:
            raise \
                RuntimeError(
                    'workspace {} failed with error code {}'.
                    format(path, msg.get_error()))

    def create_storage(self, stid, properties):
        if not isinstance(properties, dict) or \
            properties.get('is.yaks.storage.selector') is None:
            raise ValidationError("Missing Storage Selector!!")
        if not isinstance(stid, str):
            stid = str(stid)
        storage_selector = properties.get('is.yaks.storage.selector')
        properties.pop('is.yaks.storage.selector')
        if not isinstance(storage_selector, Selector):
            storage_selector = Selector(storage_selector)
        create_msg = MessageCreate(EntityType.STORAGE, storage_selector)
        if properties:
            for k in properties:
                v = properties.get(k)
                create_msg.add_property(k, v)
        var = MVar()
        self.send_queue.put((create_msg, var))
        msg = var.get()
        if self.check_msg(msg, create_msg.corr_id):
            sid = msg.get_property('is.yaks.storage.id')
            self.storages.update({stid: sid})
            return stid
        else:
            raise \
                RuntimeError(
                    'create_storage {} failed with error code {}'
                    .format(stid, msg.get_error()))

    def remove_storage(self, stid):
        self.check_connection()
        var = MVar()
        sid = self.storages.get(stid)
        if sid is None:
            raise ValidationError(
                "Storage with id {} does not exist!".format(stid))
        msg = MessageDelete(sid, EntityType.STORAGE)
        self.send_queue.put((msg, var))
        r = var.get()
        if YAKS.check_msg(r, msg.corr_id):
            return True
        return False
