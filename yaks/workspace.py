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

from yaks.encoding import Encoding, TranscodingFallback
from yaks.message import GetM, PutM, DeleteM, UnsubscribeM, SubscribeM
from yaks.message import RegisterEvalM, UnregisterEvalM, EvalM, Message
from papero.property import *
from yaks.runtime import check_reply_is_ok, check_reply_is_values
from yaks.path import Path
from yaks.selector import Selector


class Workspace(object):
    def __init__(self, runtime, path, wsid):
        self.rt = runtime
        self.path = Path.to_path(path)
        self.wsid = wsid
        self.properties = [Property(Message.WSID, wsid)]

    def put(self, path, value, quorum=1):
        path = Path.to_path(path)
        pm = PutM(self.wsid, [(path, value)])
        reply = self.rt.post_message(pm).get()
        return check_reply_is_ok(reply, pm)

    def update(self, path, value, quorum=1):
        raise NotImplementedError("Update not yet...")

    def get(self, selector, quorum=1, encoding=Encoding.RAW,
                fallback=TranscodingFallback.KEEP):
        """Requests Yaks to get a list of the stored paths/values where
            all the paths match the selector [s].
           [s] can be absolute or relative to the workspace [w].
           The [quorum] (default value is 1) is used by Yaks
           to decide for each matching path the number of
           answer from storages to wait before returning the associated value.
           The [encoding] indicates the expected encoding of the
           resulting values.
            If the original values have a different encoding,
             Yaks will try to transcode them into the expected encoding.
           By default, if no encoding is specified,
            the vaules are returned with their original encoding.
           The [fallback] indicates the action that Yaks will perform
            if the transcoding of a value fails. *)
        """
        s = Selector.to_selector(selector)
        gm = GetM(self.wsid, s)
        reply = self.rt.post_message(gm).get()
        if check_reply_is_values(reply, gm):
            return reply.kvs
        else:
            raise "Get received an invalid reply"
        return []

    def remove(self, path, quorum=1):
        """

        """
        path = Path.to_path(path)
        rm = DeleteM(self.wsid, path)
        reply = self.rt.post_message(rm).get()
        return check_reply_is_ok(reply, rm)

    def subscribe(self, selector, listener=None):
        s = Selector.to_selector(selector)
        sm = SubscribeM(self.wsid, s)
        reply = self.rt.post_message(sm).get()
        if check_reply_is_ok(reply, sm):
            subid = find_property(Message.SUBID, reply.properties)
            if listener is not None:
                self.rt.add_listener(subid, listener)
            return subid
        else:
            raise "Subscribe received an invalid reply"

    def unsubscribe(self, subscription_id):
        um = UnsubscribeM(self.wsid, subscription_id)
        reply = self.rt.post_message(um).get()
        if check_reply_is_ok(reply, um):
            self.rt.remove_listener(subscription_id)
            return True
        else:
            raise "Unsubscribe received an invalid reply"

    def register_eval(self, path, callback):
        path = Path.to_path(path)
        rem = RegisterEvalM(self.wsid, path)
        reply = self.rt.post_message(rem).get()
        if check_reply_is_ok(reply, rem):
            self.rt.add_eval_callback(path, callback)
            return True
        else:
            raise "Register_eval received an invalid reply"

    def unregister_eval(self, path):
        path = Path.to_path(path)
        uem = UnregisterEvalM(self.wsid, path)
        reply = self.rt.post_message(uem).get()
        if check_reply_is_ok(reply, uem):
            self.rt.remove_eval_callback(path)
            return True
        else:
            raise "Unregister_eval received an invalid reply"

    def eval(self, selector, multiplicity=1, encoding=Encoding.RAW,
             fallback=TranscodingFallback.KEEP):
        s = Selector.to_selector(selector)
        em = EvalM(self.wsid, s)
        reply = self.rt.post_message(em).get()
        if check_reply_is_values(reply, em):
            return reply.kvs
        else:
            raise "Get received an invalid reply"
        return []
