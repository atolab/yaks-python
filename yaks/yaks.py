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


from yaks.runtime import check_reply_is_ok, socket, send_msg, Runtime, recv_msg
from yaks.workspace import Workspace
from yaks.message import LoginM, LogoutM, WorkspaceM, Message
from papero import find_property
from yaks.admin import *
from papero import IOBuf
from mvar import MVar
import threading


class Yaks(object):
    DEFAULT_PORT = 7887

    def __init__(self, rt):
        self.rt = rt
        self.mbox = MVar()

    @staticmethod
    def login(locator, properties=None, on_close=lambda z: z, lease=0):
        '''

        Establish a session with the Yaks instance reachable through the
        provided *locator*.

        Valid format for the locator are valid  IP addresses as well
        as the combination IP:PORT.

        '''
        addr, _, p = locator.partition(':')
        if p == '':
            port = Yaks.DEFAULT_PORT
        else:
            port = int(p)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setblocking(1)
        sock.connect((addr, port))

        wbuf = IOBuf()
        lbuf = IOBuf()
        login = LoginM(properties)
        send_msg(sock, login, wbuf, lbuf)
        m = recv_msg(sock, lbuf)
        # y = None
        if check_reply_is_ok(m, login):
            rt = Runtime(sock, locator, on_close)
        rt.start()
        return Yaks(rt)

    def workspace(self, path):
        '''

        Creates a workspace relative to the provided **path**.
        Any *put* or *get* operation with relative paths on this workspace
        will be prepended with the workspace *path*.

        '''

        wsm = WorkspaceM(path)
        reply =  \
            self.rt.post_message(wsm, self.mbox).get()
        ws = None
        wsid = None
        if check_reply_is_ok(reply, wsm):
            wsid = find_property(Message.WSID, reply.properties)
            if wsid is None:
                raise "Workspace id was not provided by YAKS"
            else:
                ws = Workspace(self.rt, path, wsid)
        return ws

    def logout(self):
        '''
        Terminates this session.
        '''
        self.rt.close()
        # lom = LogoutM()
        # reply = self.rt.post_message(lom).get()
        # if check_reply_is_ok(reply, lom):

    def admin(self):
        '''

        Creates an admin workspace that provides helper operations to
        administer Yaks.

        '''
        return Admin(self.workspace(
            '/{}/{}'.format(Admin.PREFIX, Admin.MY_YAKS)))
