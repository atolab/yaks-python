import socket 
import uuid
import os
from papero import *
from mvar import MVar
from yaks.codec import *
from yaks.message import *
import threading
import logging
import sys
import traceback 

def get_frame_len(sock):
    buf = IOBuf()
    v = 0xff    
    while v > 0x7f:         
        b = sock.recv(1)
        v = byte_to_int(b)
        buf.put(v) 
    
    return buf.get_vle()

def recv_msg(sock):
    flen = get_frame_len(sock)
    
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

def send_msg(sock, msg):
    buf = IOBuf()
    encode_message(buf, msg)    
    lbuf = IOBuf(16)
    l = buf.write_pos
    lbuf.put_vle(l)
    sock.send(lbuf.get_raw_bytes())
    sock.send(buf.get_raw_bytes())

def get_log_level():
    l = logging.ERROR
    i = 0
    for a in sys.argv:
        if a.startswith('--log='):
            _,_,lvl = a.partition('=')
            l = getattr(logging, lvl.upper())
        elif a == '-l':
            l = getattr(logging, sys.argv[i+1].upper())        
        i +=1
    return l            

def check_reply_is_ok(reply, msg):
    if reply.mid == Message.OK and msg.corr_id == reply.corr_id:
        return True
    elif reply.mid == Message.ERROR:
        raise 'Yaks refused connection because of {}'.format(reply.error_code)
    else:
        raise 'Yaks replied with unexpected message'

def check_reply_is_values(reply, msg):
    if reply.mid == Message.VALUES and msg.corr_id == reply.corr_id:
        return True
    elif reply.mid == Message.ERROR:
        raise 'Yaks refused connection because of {}'.format(reply.error_code)
    else:
        raise 'Yaks replied with unexpected message'    
        
class Runtime(threading.Thread):    
    DEFAULT_TIMEOUT = 5
    def __init__(self,  sock, locator, on_close):
        threading.Thread.__init__(self)                
        self.connected = True        
        self.posted_messages = {}
        self.sock = sock
        self.running = True        
        self.on_close = on_close         
        self.logger = logging.getLogger('is.yaks')
        self.log_level = get_log_level()
        self.logger.setLevel(self.log_level)        
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)        
        self.logger.addHandler(ch)
        
        
    def close(self):       
        send_msg(self.sock, LogoutM()) 
        self.on_close(self)
        self.running = False
        self.sock.close() 


    def post_message(self, msg):
        mbox = MVar()        
        self.posted_messages[msg.corr_id] = mbox
        send_msg(self.sock, msg)
        return mbox             

    
    def notify_listeners(self, m):
        print("LISTENERS NOT COMPLETELY IMPLEMENTED YET")

    def execute_eval(self, m): 
        print("EVAL NOT COMPLETELY IMPLEMENTED YET")        
    
    def handle_reply(self, m):
        mvar = self.posted_messages.get(m.corr_id)
        if mvar is not None:                
            mvar.put(m)
            self.posted_messages.pop(m.corr_id)
        else:                    
            self.logger.debug('>> Received msg  with corr-id for which we have nothing pending: {}'.format(m.corr_id))
        
    def handle_unexpected_message(self, m):
        self.logger.warning('>> Received unexpected message with id {} -- ignoring'.format(m.mid))

    def run(self):                        
        try:
            while self.running:                                    
                m = recv_msg(self.sock)                                
                self.logger.debug('>> Received msg with id: {}'.format(m.mid))
                {
                    Message.NOTIFY: lambda m: self.notify_listeners(m),
                    Message.EVAL: lambda m: self.execute_eval(m),
                    Message.OK : lambda m: self.handle_reply(m),                    
                    Message.VALUES : lambda m: self.handle_reply(m),
                    Message.ERROR : lambda m: self.handle_reply(m)
                }.get(m.mid, lambda m: self.handle_unexpected_message(m))(m)                                
                
        except Exception as e:
            traceback.print_stack(e)
            print('Terminating the runloop because of {}'.format(e))
            self.logger.debug('Terminating the runloop because of {}'.format(e))


