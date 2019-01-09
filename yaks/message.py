'''

7 6 5 4 3 2 1 0
+-+-+-+-+-+-+-+-+ ----------------------+
|  MESSAGE CODE |    8bit               |
+-+-+-+-+-+-+-+-+                       |
|X|X|X|X|X|A|S|P|    8bit               +--> Header
+-+-+-+-+-+-+-+-+                       |
~   Corr. ID    ~  VLE max 64bit        |
+---------------+                       |
~   Properties  ~ --> Present if P = 1  |
+---------------+ ----------------------+
~     Body      ~ --> its structure depends on the message code
+---------------+


WIRE MESSAGE for framing on TCP/IP:

 7 6 5 4 3 2 1 0
+-+-+-+-+-+-+-+-+
~    Length     ~ VLE max 64bit
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
from papero import Property
import random
import json
import hexdump
from enum import Enum
from yaks.value import Value
from yaks.path import Path
from yaks.selector import Selector
from yaks.encoding import *


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

    def __init__(self, mid):
        self.mid = mid

class Header(Message):
    P_FLAG = 0x01
    FLAGS_MASK = 0x01

    @staticmethod    
    def has_flag(h, f):    
        return h & f != 0
    
    def __init__(self, mid, corr_id = None, properties=None):        
        super(Header, self).__init__(mid)
        if corr_id is None:
            self.corr_id =  random.getrandbits(16)
        else:
            self.corr_id = corr_id
        self.flags = 0
        self.properties = properties
        if properties is not None:
            self.flags = Header.P_FLAG

    def has_properties(self):
        return self.flags & Header.P_FLAG != 0

class LoginM(Header):
    def __init__(self, properties=None):
        super(LoginM,self).__init__(Message.LOGIN, properties)

class LogoutM(Header):
    def __init__(self):
        super(LogoutM,self).__init__(Message.LOGOUT)

class WorkspaceM(Header):
    def __init__(self, path, properties=None):
        super(WorkspaceM, self).__init__(Message.WORKSPACE, properties)
        self.path = path

class WorkspaceMessage(Header):
    def __init__(self, mid, wsid, properties=None):
        if properties is None:
            properties = []
        super(WorkspaceMessage, self).__init__(mid, properties.append(Property(Message.WSID, wsid)))
        self.wsid = wsid
                
class PutM(WorkspaceMessage):
    def __init__(self, wsid, path, value):        
        super(PutM, self).__init__(Message.PUT, wsid)        
        self.path = path
        self.value = value

class GetM(WorkspaceMessage):
    def __init__(self, wsid, selector):        
        super(GetM, self).__init__(Message.GET, wsid)        
        self.selector = str(selector)

class UpdateM(WorkspaceMessage):
    def __init__(self, wsid, path, value):
        super(UpdateM, self).__init__(Message.UPDATE, wsid)        
        self.path = path
        self.value = value
        
class DeleteM(WorkspaceMessage):
    def __init__(self, wsid, path, value):
        super(DeleteM, self).__init__(Message.DELETE, wsid)        
        self.path = path

class SubscribeM(WorkspaceMessage):
    def __init__(self, wsid, selector):
        super(SubscribeM, self).__init__(Message.SUB, wsid)        
        self.selector = str(selector)

class UnsubscribeM(WorkspaceMessage):
    def __init__(self, wsid, subid):
        super(UnsubscribeM, self).__init__(Message.UNSUB, wsid)        
        self.subid = subid

class EvalM(WorkspaceMessage):
    def __init__(self, wsid, path):
        super(EvalM, self).__init__(Message.EVAL, wsid)        
        self.path = path

class ValuesM(Header):
    def __init__(self, kvs):
        super(ValuesM, self).__init__(Message.VALUES)        
        self.kvs = kvs
    
    @staticmethod
    def make(header, kvs):
        vs = ValuesM(kvs)
        vs.corr_id = header.corr_id

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
    def __init__(self, error_code):
        super(ErrorM, self).__init__(Message.ERROR)        
        self.error_code = error_code

    @staticmethod
    def make(corr_id, error_code, properties=None):
        e = ErrorM(error_code)
        e.corr_id = corr_id        
        e.properties = properties
        return e 
