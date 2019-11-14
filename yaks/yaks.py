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
from zenoh import Zenoh, Z_INFO_PEER_PID_KEY


class Yaks(object):
    '''

    The Yaks client API.

    '''

    ZENOH_DEFAULT_PORT = 7447

    def __init__(self, rt):
        self.rt = rt

    @staticmethod
    def login(locator, properties=None):
        '''

        Establish a session with the Yaks instance reachable via provided
        Zenoh locator. If the provided locator is ``None``, :func:`login`
        will perform some dynamic discovery and try to establish the session
        automatically. When not ``None``, the locator must have the format:
        ``tcp/<ip>:<port>``.

        :param locator: a Zenoh locator or ``None``.
        :param properties: the Properties to be used for this session
            (e.g. "user", "password", ...). Can be ``None``.
        :returns: a Yaks object.

        '''
        zprops = {} if properties is None else {
            zenoh.Z_USER_KEY if k == "user" else zenoh.Z_PASSWORD_KEY: val
            for k, val in properties.items()
            if k == "user" or key == "password"}

        return Yaks(Zenoh.open(locator, zprops))

    def workspace(self, path, executor=None):
        '''

        Creates a :class:`~yaks.workspace.Workspace` using the
        provided path. All relative Selector or Path used with this
        :class:`~yaks.workspace.Workspace` will be relative to
        this path.

        :param path: the Workspace's path.
        :param executor: an executor of type
            :py:class:`concurrent.futures.Executor` or ``None``.
            If not ``None``, all subscription listeners and eval callbacks are
            executed by the provided executor. This is useful when listeners
            and/or callbacks need to perform long operations or need to call
            operations like :func:`~yaks.workspace.Workspace.get`.
        :returns: a :class:`~yaks.workspace.Workspace`.

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
                        self.rt.info()[Z_INFO_PEER_PID_KEY]))))
