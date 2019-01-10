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


class Admin(object):

    PREFIX = '@'
    MY_YAKS = 'local'

    def __init__(self, ws):
        self.ws = ws

    def add_frontend(self, feid, properties, yaks=MY_YAKS):
        path = '/{}/{}/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        value = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(path, value, quorum=1)

    def get_frontends(self, yaks=MY_YAKS):
        s = '/{}/{}/frontend/*'.format(Admin.PREFIX, yaks)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def get_frontend(self, feid, yaks=MY_YAKS):
        s = '/{}/{}/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            return kvs[0][1].value
        return None

    def remove_frontend(self, feid, yaks=MY_YAKS):
        path = '/{}/{}/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        return self.ws.remove(path, quorum=1)

    def add_backend(self, beid, properties, yaks=MY_YAKS):
        path = '/{}/{}/backend/{}'.format(Admin.PREFIX, yaks, beid)
        value = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(path, value, quorum=1)

    def get_backends(self, yaks=MY_YAKS):
        s = '/{}/{}/backend/*'.format(Admin.PREFIX, yaks)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def get_backend(self, beid, yaks=MY_YAKS):
        s = '/{}/{}/backend/{}'.format(Admin.PREFIX, yaks, beid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            return kvs[0][1].value
        return None

    def remove_backend(self, beid, yaks=MY_YAKS):
        path = '/{}/{}/backend/{}'.format(Admin.PREFIX, yaks, beid)
        return self.ws.remove(path, quorum=1)

    def add_storage(self, stid, properties, beid=None, yaks=MY_YAKS):
        if not beid:
            beid = 'auto'
        p = '/{}/{}/backend/{}/storage/{}'.format(
            Admin.PREFIX, yaks, beid, stid)
        v = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(p, v, quorum=1)

    def get_storages(self, beid=None, yaks=MY_YAKS):
        if not beid:
            beid = '*'
        s = '/{}/{}/backend/{}/storage/*'.format(Admin.PREFIX, yaks, beid)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def get_storage(self, stid, yaks=MY_YAKS):
        s = '/{}/{}/backend/*/storage/{}'.format(Admin.PREFIX, yaks, stid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            return kvs[0][1].value
        return None

    def remove_storage(self, stid, yaks=MY_YAKS):
        s = '/{}/{}/backend/*/storage/{}'.format(Admin.PREFIX, yaks, stid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            p = kvs[0][0]
            return self.ws.remove(p, quorum=1)
        return False

    def get_sessions(self, yaks=MY_YAKS, feid=None):
        if not feid:
            feid = '*'
        s = '/{}/{}/frontend/{}/session/*'.format(Admin.PREFIX, yaks, feid)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))

    def close_session(self, sid, yaks=MY_YAKS):
        s = '/{}/{}/frontend/*/session/{}'.format(Admin.PREFIX, yaks, sid)
        kvs = self.ws.get(s)
        if len(kvs) > 0:
            p = kvs[0][0]
            return self.ws.remove(p, quorum=1)
        return False

    def get_subscriptions(self, sid, yaks=MY_YAKS):
        s = '/{}/{}/frontend/*/session/{}'.format(Admin.PREFIX, yaks, sid)
        kvs = self.ws.get(s)
        return list(map(lambda e: (e[0].split('/')[-1], e[1].value), kvs))
