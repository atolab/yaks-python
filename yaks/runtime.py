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
# Contributors: Angelo Corsaro, ADLINK Technology Inc. - Yaks API refactoring

import socket
import uuid
import os
import threading
import logging
import sys
import traceback
from yaks.logger import APILogger
from papero import *
from mvar import MVar
from yaks.codec import decode_message, encode_message
from yaks.message import Message, ErrorM, LogoutM, ValuesM
from queue import Queue

SND_QUEUE_LEN = 128
RCV_QUEUE_LEN = 128


def get_frame_len(sock, buf):
    buf.clear()
    v = 0xff
    while v > 0x7f:
        b = sock.recv(1)
        v = byte_to_int(b)
        buf.put(v)

    return buf.get_vle()


def recv_msg(sock, lbuf):
    lbuf.clear()
    try:
        flen = get_frame_len(sock, lbuf)

        bs = sock.recv(flen)
        n = len(bs)
        while n < flen:
            m = flen - n
            cs = sock.recv(m)
            n = n + len(cs)
            bs = bs + cs

        rbuf = IOBuf.from_bytes(bs)
        m = decode_message(rbuf)
        return m
    except OSError:
        m = ErrorM(0)
        return m


def send_msg(sock, msg, buf, lbuf):
    buf.clear()
    lbuf.clear()
    encode_message(buf, msg)
    length = buf.write_pos
    lbuf.put_vle(length)
    sock.sendall(lbuf.get_raw_bytes())
    sock.sendall(buf.get_raw_bytes())


def get_log_level():
    log_level = logging.ERROR
    i = 0
    for a in sys.argv:
        if a.startswith('--log='):
            _, _, lvl = a.partition('=')
            log_level = getattr(logging, lvl.upper())
        elif a == '-l':
            log_level = getattr(logging, sys.argv[i + 1].upper())
        i += 1
    return log_level


def check_reply_is_ok(reply, msg):
    if reply.mid == Message.OK and msg.corr_id == reply.corr_id:
        return True
    elif reply.mid == Message.ERROR:
        raise RuntimeError(
            'Yaks refused connection because of {}'.format(reply.error_code))
    else:
        err_msg = 'Yaks replied with unexpected message '\
            ' R_MID: {} R_CORRID: {} != E_MID: {} E_CORRID: {}'\
            .format(reply.mid, reply.corr_id, Message.OK, msg.corr_id)
        raise RuntimeError(err_msg)


def check_reply_is_values(reply, msg):
    if reply.mid == Message.VALUES and msg.corr_id == reply.corr_id:
        return True
    elif reply.mid == Message.ERROR:
        raise RuntimeError(
            'Yaks refused connection because of {}'.format(reply.error_code))
    else:
        err_msg = 'Yaks replied with unexpected message '\
            ' R_MID: {} R_CORRID: {} != E_MID: {} E_CORRID: {}'\
            .format(reply.mid, reply.corr_id, Message.VALUES, msg.corr_id)
        raise RuntimeError(err_msg)


class Runtime(threading.Thread):

    DEFAULT_TIMEOUT = 5

    def __init__(self, sock, locator, on_close):
        threading.Thread.__init__(self)
        self.logger = APILogger(get_log_level(), False)
        self.daemon = True
        self.connected = True
        self.posted_messages = {}
        self.sock = sock
        self.running = True
        self.on_close = on_close
        self.listeners = {}
        self.eval_callbacks = {}
        self.putMbox = MVar()
        self.rtMbox = MVar()
        self.evalMBox = MVar()
        self.tss = {}
        self.wlbuf = IOBuf()
        self.wbuf = IOBuf()
        self.rlbuf = IOBuf()
        self.wlbuf = IOBuf()
        self.snd_queue = Queue(SND_QUEUE_LEN)
        self.snd_thread = threading.Thread(target=self.send_loop)
        self.snd_thread.setDaemon(True)
        self.snd_thread.start()

        self.notification_queue = Queue(RCV_QUEUE_LEN)
        self.notify_thread = threading.Thread(target=self.notify_loop)
        self.notify_thread.setDaemon(True)
        self.notify_thread.start()

    def send_loop(self):
        try:
            while True:
                msg = self.snd_queue.get()
                send_msg(self.sock, msg, self.wbuf, self.wlbuf)
        except Exception as e:
            traceback.print_exc()
            self.logger.debug('run()',
                              'Terminating the send-loop because of {}'
                              .format(e))

    def close(self):
        self.post_message(LogoutM(), self.rtMbox).get()
        self.on_close(self)
        self.running = False
        self.sock.close()

    def post_message(self, msg, mbox):
        self.posted_messages.update({msg.corr_id: (mbox, [])})
        self.snd_queue.put(msg)
        return mbox

    def post_message_no_reply(self, msg):
        self.snd_queue.put(msg)

    def add_listener(self, subid, callback):
        self.listeners.update({subid: callback})

    def remove_listener(self, subid):
        if subid in self.listeners.keys():
            self.listeners.pop(subid)

    def add_eval_callback(self, path, callback):
        self.eval_callbacks.update({path: callback})

    def remove_eval_callback(self, path):
        if path in self.eval_callbacks.keys():
            self.eval_callbacks.pop(path)

    def notify_listeners(self, m):
        subid = m.subid
        listener = self.listeners.get(subid)
        if listener is not None:
            listener(m.kvs)

    def notify_loop(self):
        while True:
            m = self.notification_queue.get()
            self.notify_listeners(m)

    def execute_eval(self, m):
        selector = m.selector
        for path in self.eval_callbacks:
            if selector.is_prefixed_by_path(path):
                cb = self.eval_callbacks.get(path)
                p = selector.get_path()
                args = selector.dict_from_properties()
                # TODO: should be called in another thread

                def eval_cb_adaptor(path, p, args, cid):
                    try:
                        kvs = [(path, cb(p, **args))]
                        vm = ValuesM(kvs)
                        vm.corr_id = cid
                        reply = self.post_message(vm, self.evalMBox).get()
                        if not check_reply_is_ok(reply, vm):
                            raise ValueError('YAKS error on EVAL')
                    except (Exception, RuntimeError):
                        self.post_message(ErrorM.make(cid, ErrorM.BAD_REQUEST),
                                                        self.evalMBox)

                eval_th = threading.Thread(target=eval_cb_adaptor,
                                           args=(path, p, args, m.corr_id))
                eval_th.start()

    def consolidate_reply(self, ms):
        ckvs = []
        for m in ms:
            ckvs = ckvs + m.kvs

        m = ms[len(ms) - 1]
        m.kvs = ckvs
        return m

    def handle_reply(self, m):
        map_value = self.posted_messages.get(m.corr_id)
        if map_value is None:
            self.logger.warning('handle_reply()',
                                '>> Received not matching message {}'
                                .format(m.corr_id))
            return
        self.logger.warning('handle_reply()',
                                '>> Received matching message {}'
                                .format(m.corr_id))
        (mvar, partial) = map_value
        if mvar is not None:
            if m.mid == Message.VALUES:
                if m.is_complete():
                    self.logger.warning('handle_reply()',
                                        '>> Complete message received {}'
                                        .format(m.corr_id))
                    if len(partial) > 0:
                        partial.append(m)
                        m = self.consolidate_reply(partial)
                    mvar.put(m)
                    self.posted_messages.pop(m.corr_id)
                else:
                    self.logger.warning('handle_reply()',
                                        '>> Partial message received {}'
                                        .format(m.corr_id))
                    partial.append(m)
                    self.posted_messages.update({m.corr_id: (mvar, partial)})

            else:
                mvar.put(m)
                self.posted_messages.pop(m.corr_id)

    def handle_unexpected_message(self, m):
        self.logger.warning('handle_unexpected_message()',
                            '>> Received unexpected message with id {}\
                             -- ignoring'
                            .format(m.mid))

    def run(self):
        try:
            while self.running:
                m = recv_msg(self.sock, self.rlbuf)
                {
                    Message.NOTIFY: lambda m: self.notification_queue.put(m),
                    Message.EVAL: lambda m: self.execute_eval(m),
                    Message.OK: lambda m: self.handle_reply(m),
                    Message.VALUES: lambda m: self.handle_reply(m),
                    Message.ERROR: lambda m: self.handle_reply(m)
                }.get(m.mid, lambda m: self.handle_unexpected_message(m))(m)

        except Exception as e:
            traceback.print_exc()
            self.logger.debug('run()',
                              'Terminating the receive-loop because of {}'
                              .format(e))
