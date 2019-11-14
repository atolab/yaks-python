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

from yaks.value import Value
from yaks.encoding import Encoding
import zenoh


class Admin(object):
    '''
    The Administration helper class.
    '''

    PREFIX = '@'

    def __init__(self, ws):
        self.ws = ws
        self.local = ''.join('{:02x}'.format(x) for x in
                             ws.rt.info()[zenoh.Z_INFO_PEER_PID_KEY])

    def add_backend(self, beid, properties, yaks=None):
        '''
        Add a backend in the specified Yaks.

        :param beid: the Id of the backend.
        :param propertiers: some configuration for the backend.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        path = '/{}/{}/plugins/yaks/backend/{}'.format(
            Admin.PREFIX, yaks, beid)
        value = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(path, value)

    def get_backends(self, yaks=None):
        '''
        Get all the backends from the specified Yaks.

        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/*'.format(
            Admin.PREFIX, yaks)
        entries = self.ws.get(s)
        return list(map(
            lambda e: (e.get_path().split('/')[-1],
                       e.get_value().value), entries))

    def get_backend(self, beid, yaks=None):
        '''
        Get backend's properties from the specified Yaks.

        :param beid: the Id of the backend.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/{}'.format(
            Admin.PREFIX, yaks, beid)
        entries = self.ws.get(s)
        if len(entries) > 0:
            return entries[0].get_value().value
        return None

    def remove_backend(self, beid, yaks=None):
        '''
        Remove a backend from the specified Yaks.

        :param beid: the Id of the backend.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        path = '/{}/{}/plugins/yaks/backend/{}'.format(
            Admin.PREFIX, yaks, beid)
        return self.ws.remove(path)

    def add_storage(self, stid, properties, beid=None, yaks=None):
        '''
        Adds a storage in the specified Yaks backend.

        :param stid: the Id of the storage.
        :param propertiers: some configuration for the storage.
        :param beid: the Id of the backend. If ``None``, a backend is
            automatically selected.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        if not beid:
            beid = 'auto'
        p = '/{}/{}/plugins/yaks/backend/{}/storage/{}'.format(
            Admin.PREFIX, yaks, beid, stid)
        v = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(p, v)

    def get_storages(self, beid=None, yaks=None):
        '''
        Adds a storage in the specified Yaks.

        :param beid: the Id of the backend. If ``None``, all backends.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        if not beid:
            beid = '*'
        s = '/{}/{}/plugins/yaks/backend/{}/storage/*'.format(
            Admin.PREFIX, yaks, beid)
        entries = self.ws.get(s)
        return list(map(
            lambda e: (e.get_path().split('/')[-1],
                       e.get_value().value), entries))

    def get_storage(self, stid, yaks=None):
        '''
        Get storage's properties from the specified Yaks.

        :param stid: the Id of the storage.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/*/storage/{}'.format(
            Admin.PREFIX, yaks, stid)
        entries = self.ws.get(s)
        if len(entries) > 0:
            return entries[0].get_value().value
        return None

    def remove_storage(self, stid, yaks=None):
        '''
        Remove a backend from the specified Yaks.

        :param stid: the Id of the storage.
        :param yaks: the UUID of the Yaks instance. If ``None``, the local
            Yaks instance.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/*/storage/{}'.format(
            Admin.PREFIX, yaks, stid)
        entries = self.ws.get(s)
        if len(entries) > 0:
            p = entries[0].get_path()
            return self.ws.remove(p)
        return False
