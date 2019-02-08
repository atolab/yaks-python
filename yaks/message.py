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
#
#
#
# 7 6 5 4 3 2 1 0
# +-+-+-+-+-+-+-+-+ ----------------------+
# |  MESSAGE CODE |    8bit               |
# +-+-+-+-+-+-+-+-+                       |
# |X|X|X|X|X|A|S|P|    8bit               +--> Header
# +-+-+-+-+-+-+-+-+                       |
# ~   Corr. ID    ~  VLE max 64bit        |
# +---------------+                       |
# ~   Properties  ~ --> Present if P = 1  |
# +---------------+ ----------------------+
# ~     Body      ~ --> its structure depends on the message code
# +---------------+
#
#
# WIRE MESSAGE for framing on TCP/IP:
#
#  7 6 5 4 3 2 1 0
# +-+-+-+-+-+-+-+-+
# ~    Length     ~ VLE max 64bit
# +-+-+-+-+-+-+-+-+ ----------------------+
# |  MESSAGE CODE |    8bit               |
# +-+-+-+-+-+-+-+-+                       |
# |X|X|X|X|X|A|S|P|    8bit               +--> Header
# +-+-+-+-+-+-+-+-+                       |
# ~    Corr. id   ~  VLE max 64bit        |
# +---------------+                       |
# ~   Properties  ~ --> Present if P = 1  |
# +---------------+ ----------------------+
# ~     Body      ~ VL
# +---------------+
#


from papero import Property, find_property
import random
import json
import hexdump
from enum import Enum
from yaks.value import Value
from yaks.path import Path
from yaks.selector import Selector


class Message(object):
    LOGIN = 0x01
    LOGOUT = 0x02
    WORKSPACE = 0x03

    PUT = 0xA0
    UPDATE = 0xA1
    GET = 0xA2
    DELETE = 0xA3

    SUB = 0xB0
    UNSUB = 0xB1
    NOTIFY = 0xB2

    REG_EVAL = 0xC0
    UNREG_EVAL = 0xC1
    EVAL = 0xC2

    OK = 0xD0
    VALUES = 0xD1

    ERROR = 0xE0

    WSID = "wsid"
    AUTO = "auto"
    SUBID = "subid"

    def __init__(self, mid):
        self.mid = mid


class Header(Message):
    # Property Flag
    P_FLAG = 0x01
    # Incomplete Result
    # This flag is only relevant for values.
    I_FLAG = 0x02
    FLAGS_MASK = 0x01

    @staticmethod
    def has_flag(h, f):
        return h & f != 0

    def __init__(self, mid, flags=0, corr_id=random.getrandbits(16),
                 properties=None):
        super(Header, self).__init__(mid)

        self.corr_id = corr_id
        self.flags = flags
        self.properties = properties
        if properties is not None:
            self.flags = self.flags | Header.P_FLAG

    def has_properties(self):
        return self.flags & Header.P_FLAG != 0

    def is_complete(self):
        return self.flags & Header.I_FLAG == 0


class LoginM(Header):
    def __init__(self, properties=None):
        super(LoginM, self).__init__(Message.LOGIN, properties=properties)


class LogoutM(Header):
    def __init__(self):
        super(LogoutM, self).__init__(Message.LOGOUT)


class WorkspaceM(Header):
    def __init__(self, path, properties=None):
        super(WorkspaceM, self).__init__(Message.WORKSPACE,
                                         properties=properties)
        self.path = path


class WorkspaceMessage(Header):
    def __init__(self, mid, wsid, properties=None):
        if properties is None:
            properties = []
        properties.append(Property(Message.WSID, wsid))
        super(WorkspaceMessage, self).__init__(mid, properties=properties)
        self.wsid = wsid


class PutM(WorkspaceMessage):
    def __init__(self, wsid, kvs, properties=None):
        super(PutM, self).__init__(Message.PUT, wsid, properties)
        self.kvs = kvs

    @staticmethod
    def make(kvs, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return PutM(wsid, kvs, properties)


class GetM(WorkspaceMessage):
    def __init__(self, wsid, selector, properties=None):
        super(GetM, self).__init__(Message.GET, wsid, properties)
        self.selector = selector

    @staticmethod
    def make(selector, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return GetM(wsid, selector, properties)


class UpdateM(WorkspaceMessage):
    def __init__(self, wsid, kvs, properties=None):
        super(UpdateM, self).__init__(Message.UPDATE, wsid, properties)
        self.kvs = kvs

    @staticmethod
    def make(kvs, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return UpdateM(wsid, kvs, properties)


class DeleteM(WorkspaceMessage):
    def __init__(self, wsid, path, properties=None):
        super(DeleteM, self).__init__(Message.DELETE, wsid, properties)
        self.path = path

    @staticmethod
    def make(path, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return DeleteM(wsid, path, properties)


class SubscribeM(WorkspaceMessage):
    def __init__(self, wsid, selector, properties=None):
        super(SubscribeM, self).__init__(Message.SUB, wsid, properties)
        self.selector = selector

    @staticmethod
    def make(selector, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return SubscribeM(wsid, selector, properties)


class UnsubscribeM(WorkspaceMessage):
    def __init__(self, wsid, subid, properties=None):
        super(UnsubscribeM, self).__init__(Message.UNSUB, wsid, properties)
        self.subid = subid

    @staticmethod
    def make(subid, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return UnsubscribeM(wsid, subid, properties)


class NotifyM(WorkspaceMessage):
    def __init__(self, wsid, subid, kvs, properties=None):
        super(NotifyM, self).__init__(Message.NOTIFY, wsid, properties)
        self.subid = subid
        self.kvs = kvs

    @staticmethod
    def make(subid, kvs, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return NotifyM(wsid, subid, kvs, properties)


class EvalM(WorkspaceMessage):
    def __init__(self, wsid, selector, properties=None):
        super(EvalM, self).__init__(Message.EVAL, wsid, properties)
        self.selector = selector

    @staticmethod
    def make(selector, header):
        wsid = ''
        if header.properties:
            wsid = find_property(Message.WSID, header.properties)
        m = EvalM(wsid, selector, header.properties)
        m.corr_id = header.corr_id
        return m


class RegisterEvalM(WorkspaceMessage):
    def __init__(self, wsid, path, properties=None):
        super(RegisterEvalM, self).__init__(Message.REG_EVAL, wsid, properties)
        self.path = path

    @staticmethod
    def make(path, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return RegisterEvalM(wsid, path, properties)


class UnregisterEvalM(WorkspaceMessage):
    def __init__(self, wsid, path, properties=None):
        super(UnregisterEvalM, self).__init__(
            Message.UNREG_EVAL, wsid, properties)
        self.path = path

    @staticmethod
    def make(path, properties=None):
        wsid = ''
        if properties:
            wsid = find_property(Message.WSID, properties)
        return UnregisterEvalM(wsid, path, properties)


class ValuesM(Header):
    def __init__(self, kvs):
        super(ValuesM, self).__init__(Message.VALUES)
        self.kvs = kvs

    @staticmethod
    def make(header, kvs):
        vs = ValuesM(kvs)
        vs.flags = header.flags
        vs.corr_id = header.corr_id
        return vs


class OkM(Header):
    def __init__(self):
        super(OkM, self).__init__(Message.OK)

    @staticmethod
    def make(header):
        vs = OkM()
        vs.corr_id = header.corr_id
        vs.properties = header.properties
        return vs


class ErrorM(Header):
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    PRECONDITION_FAILED = 412
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    INSUFFICIENT_STORAGE = 507

    def __init__(self, error_code):
        super(ErrorM, self).__init__(Message.ERROR)
        self.error_code = error_code

    @staticmethod
    def make(corr_id, error_code, properties=None):
        e = ErrorM(error_code)
        e.corr_id = corr_id
        e.properties = properties
        return e
