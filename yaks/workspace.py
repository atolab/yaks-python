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

    def put(self, path, value, quorum=0):
        '''

        The put operation:

        - causes the notification of all subscriptions whose selector matches
            the path parameter, and

        - stores the tuple <path,value> on all storages in YAKS whose selector
            matches the path parameter.

        Notice that the **path** can be absolute or relative to the workspace.

        If a **quorum** is provided then the put will success only if and only
        if a number quorum of independent storages exist that match path.
        If such a set exist, the put operation will complete only after
        the tuple <path,value> has been written on all these storages.

        If no quorum is provided, then no assumptions are made and the **put**
        always succeeds, even if there are currently no matching storage.
        In this case the only effect of this operation will be that of
        triggering matching subscriber, if any exist.

        '''

        path = Path.to_path(path)
        pm = PutM(self.wsid, [(path, value)])
        reply = self.rt.post_message(pm).get()
        return check_reply_is_ok(reply, pm)

    def update(self, path, value, quorum=0):
        '''

        Allows to **put** a delta,
        thus avoiding to distribute the entire value.

        '''

        raise NotImplementedError("Update not yet...")

    def get(self, selector, quorum=0, encoding=Encoding.RAW,
                fallback=TranscodingFallback.KEEP):
        '''

        gets the set of tuples  *<path,value>* available in YAKS
        for which  the path  matches the selector,
        where the selector can be absolute or relative to the workspace.

        If a **quorum** is provided, then **get** will complete succesfully
        if and only if a number **quorum** of independent and complete
        storage set exist.
        Complete storage means a storage that fully covers the selector
        (i.e. any path matching the selector is covered by the storage).
        This ensures that if there is a  *{ <path,value> }* stored in YAKS
        for which the *path* matches the selector **s**,
        then there are at least **quorum** idependent copies of this element
        stored in YAKS.
        Of these **quorum** idependent copies,
        the one returned to the application is the most recent version.

        If no quorum is provided (notice this is the default behaviour) then
        the [get] will succeed even if there isn't a set of storages that
        fully covers the selector.
        I.e. storages that partially cover the selector will also reply.

        The **encoding**  allows an application to request values to be
        encoded in a specific format.


        If no encoding is provided (this is the default behaviour) then YAKS
        will not try to perform any transcoding and will
        return matching values in the encoding in which they are stored.

        The **fallback** controls what happens for those values that cannot be
        transcoded into the desired encoding, the available options are:

        - Fail: the **get** fails if some value cannot be transcoded.
        - Drop: values that cannot be transcoded are dropped.
        - Keep: values that cannot be transcoded are kept with their original
            encoding and left for the application to deal with.

        '''

        s = Selector.to_selector(selector)
        gm = GetM(self.wsid, s)
        reply = self.rt.post_message(gm).get()
        if check_reply_is_values(reply, gm):
            return reply.kvs
        else:
            raise "Get received an invalid reply"
        return []

    def remove(self, path, quorum=0):
        '''

        Removes from all  Yaks's storages the tuples having the given **path**.
        The **path** can be absolute or relative to the workspace.
        If a **quorum** is provided, then the *remove* will
        complete only after having successfully removed the tuple
        from **quorum** storages.

        '''

        path = Path.to_path(path)
        rm = DeleteM(self.wsid, path)
        reply = self.rt.post_message(rm).get()
        return check_reply_is_ok(reply, rm)

    def subscribe(self, selector, listener=None):
        '''

        Registers a subscription to tuples whose path matches the **selector**.

        A subscription identifier is returned.
        The **selector** can be absolute or relative to the workspace.
        If specified,  the **listener callback will be called for each **put**
        and **update** on tuples whose
        path matches the subscription **selector**
        listener should expect a list of (Path, Changes)

        '''

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
        '''

        Unregisters a previous subscription with the identifier **subid**

        '''
        um = UnsubscribeM(self.wsid, subscription_id)
        reply = self.rt.post_message(um).get()
        if check_reply_is_ok(reply, um):
            self.rt.remove_listener(subscription_id)
            return True
        else:
            raise "Unsubscribe received an invalid reply"

    def register_eval(self, path, callback):
        '''

        Registers an evaluation function **eval** under the provided **path**.
        The **path** can be absolute or relative to the workspace.

        '''

        path = Path.to_path(path)
        rem = RegisterEvalM(self.wsid, path)
        reply = self.rt.post_message(rem).get()
        if check_reply_is_ok(reply, rem):
            self.rt.add_eval_callback(path, callback)
            return True
        else:
            raise "Register_eval received an invalid reply"

    def unregister_eval(self, path):
        '''

        Unregisters an previously registered evaluation function under
        the give [path].
        The [path] can be absolute or relative to the workspace.

        '''

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
        '''

        Requests the evaluation of registered evals whose registration
        **path** matches the given **selector**.

        If several evaluation function are registerd with the same path
        (by different Yaks clients), then Yaks will call N functions
        where N=[multiplicity] (default value is 1).
        Note that in such case, the returned *{ <path,value> }*
        will contain N time each matching path with the different
        values returned by each evaluation.
        The **encoding** indicates the expected encoding of the resulting
        values. If the original values have a different encoding,
        Yaks will try to transcode them into the expected encoding.
        By default, if no encoding is specified, the values are
        returned with their original encoding.
        The **fallback** indicates the action that YAKS
        will perform if the transcoding of a value fails.

        '''

        s = Selector.to_selector(selector)
        em = EvalM(self.wsid, s)
        reply = self.rt.post_message(em).get()
        if check_reply_is_values(reply, em):
            return reply.kvs
        else:
            raise "Get received an invalid reply"
        return []
