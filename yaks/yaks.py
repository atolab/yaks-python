from yaks.runtime import *
from yaks.workspace import *
from yaks.admin import *

class Yaks(object):
    DEFAULT_PORT = 7887
    def __init__(self, rt):
        self.rt = rt

    @staticmethod
    def login(locator, properties=None, on_close = lambda z : z , lease = 0):
        addr,_,p = locator.partition(':')
        if p == '':
            port = Yaks.DEFAULT_PORT
        else:
            port = int(p)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setblocking(1)
        sock.connect((addr, port))
                
        login = LoginM(properties)
        send_msg(sock, login)
        m = recv_msg(sock)        
        y = None
        if check_reply_is_ok(m, login):        
            rt = Runtime(sock, locator, on_close)                
        rt.start()        
        return Yaks(rt)

    def workspace(self, path):
        wsm  = WorkspaceM(path)        
        reply = self.rt.post_message(wsm).get()
        ws =  None
        if check_reply_is_ok(reply, wsm):
            ws = Workspace(self)
        return ws 

    def logout(self):
        lom = LogoutM()
        reply = self.rt.post_message(lom).get()
        check_reply_is_ok(reply, lom)

    def admin(self): 
        return Admin(self.workspace(Path("/@/local")))
