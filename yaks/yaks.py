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

from yaks.workspace import Workspace
from yaks.admin import *
import threading
import zenoh


class Yaks(object):
    DEFAULT_PORT = 7887
    ZENOH_DEFAULT_PORT = 7447

    def __init__(self, rt):
        self.rt = rt

    @staticmethod
    def login(locator, z_locator=None, properties=None, on_close=lambda z: z, lease=0):
        '''

        Establish a session with the Yaks instance reachable through the
        provided *locator*.

        Valid format for the locator are valid  IP addresses as well
        as the combination IP:PORT.

        ''' 
        return Yaks(zenoh.Zenoh(locator, 'user'.encode(), 'password'.encode()))

    def workspace(self, path):
        '''

        Creates a workspace relative to the provided **path**.
        Any *put* or *get* operation with relative paths on this workspace
        will be prepended with the workspace *path*.

        '''
        return Workspace(self.rt, path)

    def logout(self):
        '''

        Terminates this session.

        '''
        self.rt.close()

    def admin(self):
        '''

        Creates an admin workspace that provides helper operations to
        administer Yaks.

        '''
        return Admin(self.workspace(
            '/{}/{}'.format(
                Admin.PREFIX, 
                ''.join('{:02x}'.format(x) for x in self.rt.info()[zenoh.Z_INFO_PEER_PID_KEY]))))
