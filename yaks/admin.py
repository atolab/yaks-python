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

    PREFIX = '@'

    def __init__(self, ws):
        self.ws = ws
        self.local = ''.join('{:02x}'.format(x) for x in
                             ws.rt.info()[zenoh.Z_INFO_PEER_PID_KEY])

    def add_frontend(self, feid, properties, yaks=None):
        '''
        Not supported in this version.
        '''
        if(yaks is None):
            yaks = self.local
        path = '/{}/{}/plugins/yaks/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        value = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(path, value, quorum=1)

    def get_frontends(self, yaks=None):
        '''
        Returns the list of frontends available on the Yaks
        instance with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/frontend/*'.format(Admin.PREFIX, yaks)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def get_frontend(self, feid, yaks=None):
        '''
        Returns the frontend with the front-end ID **feid**
        on the Yaks instance with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            return kvs[0][1].value
        return None

    def remove_frontend(self, feid, yaks=None):
        '''
        Not supported in this version.
        '''
        if(yaks is None):
            yaks = self.local
        path = '/{}/{}/plugins/yaks/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        return self.ws.remove(path, quorum=1)

    def add_backend(self, beid, properties, yaks=None):
        '''
        Not supported in this version.
        '''
        if(yaks is None):
            yaks = self.local
        path = '/{}/{}/plugins/yaks/backend/{}'.format(Admin.PREFIX, yaks, beid)
        value = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(path, value, quorum=1)

    def get_backends(self, yaks=None):
        '''
        Gets the list of all available back-ends on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/*'.format(Admin.PREFIX, yaks)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def get_backend(self, beid, yaks=None):
        '''
        Gets the  back-end with id **beid** on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/{}'.format(Admin.PREFIX, yaks, beid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            return kvs[0][1].value
        return None

    def remove_backend(self, beid, yaks=None):
        '''
        Not supported in this version.
        '''
        if(yaks is None):
            yaks = self.local
        path = '/{}/{}/plugins/yaks/backend/{}'.format(Admin.PREFIX, yaks, beid)
        return self.ws.remove(path, quorum=1)

    def add_storage(self, stid, properties, beid=None, yaks=None):
        '''
        Adds a storage named **stid** on the backend **beid** and with
        storage and back-end specific configuration defined through
        **properties**.
        The **properties** should always include the selector,
        e.g., *{"selector":"/demo/astore/**"}*.
        Main memory is the default backend used when **beid** is unset.

        Finally, the storage is created on the Yaks instance with UUID
        **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        if not beid:
            beid = 'auto'
        p = '/{}/{}/plugins/yaks/backend/{}/storage/{}'.format(
            Admin.PREFIX, yaks, beid, stid)
        v = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(p, v, quorum=1)

    def get_storages(self, beid=None, yaks=None):
        '''
        Gets the list of all available storages on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        if not beid:
            beid = '*'
        s = '/{}/{}/plugins/yaks/backend/{}/storage/*'.format(Admin.PREFIX, yaks, beid)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def get_storage(self, stid, yaks=None):
        '''
        Gets the  storage with id **stid** on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/*/storage/{}'.format(Admin.PREFIX, yaks, stid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            return kvs[0][1].value
        return None

    def remove_storage(self, stid, yaks=None):
        '''
        Removes the  storage with id **stid** on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/backend/*/storage/{}'.format(Admin.PREFIX, yaks, stid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            p = kvs[0][0]
            return self.ws.remove(p, quorum=1)
        return False

    def get_sessions(self, yaks=None, feid=None):
        '''
        Gets the list of all available sessions on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        if not feid:
            feid = '*'
        s = '/{}/{}/plugins/yaks/frontend/{}/session/*'.format(Admin.PREFIX, yaks, feid)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def close_session(self, sid, yaks=None):
        '''
        Not supported in this version.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/frontend/*/session/{}'.format(Admin.PREFIX, yaks, sid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            p = kvs[0][0]
            return self.ws.remove(p, quorum=1)
        return False

    def get_subscriptions(self, sid, yaks=None):
        '''
        Gets the list of all active subscriptions on the Yaks instance
        with UUID **yaks**.
        '''
        if(yaks is None):
            yaks = self.local
        s = '/{}/{}/plugins/yaks/frontend/*/session/{}'.format(Admin.PREFIX, yaks, sid)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))
