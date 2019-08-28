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
    ZENOH_DEFAULT_PORT = 7447

    def __init__(self, rt):
        self.rt = rt

    @staticmethod
    def login(locator, properties=None,
              on_close=lambda z: z, lease=0):
        '''

        Establish a session with the Yaks instance reachable through the
        provided *locator*.

        Valid format for the locator are valid  IP addresses as well
        as the combination IP:PORT.

        '''
        user = None
        if properties is not None and "user" in properties:
            user = properties['user']
        password = None
        if properties is not None and"password" in properties:
            password = properties['password']
        return Yaks(zenoh.Zenoh(locator, user, password))

    def workspace(self, path, executor=None):
        '''

        Creates a workspace relative to the provided **path**.
        Any *put* or *get* operation with relative paths on this workspace
        will be prepended with the workspace *path*.

        If an executor of type concurrent.futures.Executor is provided,
        then all subscription listeners and eval callbacks are executed
        by the provided executor. This is useful when listners and/or
        callbacks need to perform long operations or need to call get().

        '''
        return Workspace(self.rt, path, executor)

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
                ''.join('{:02x}'.format(x) for x in
                        self.rt.info()[zenoh.Z_INFO_PEER_PID_KEY]))))
