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

    def __extract_id_v(kv):
        k, v = kv
        return (k.split('/')[-1], v.value)

    def __init__(self, ws):
        self.ws = ws

    def add_frontend(self, feid, properties, yaks=MY_YAKS):
        path = '/{}/{}/frontend/{}'.format(Admin.PREFIX, yaks, feid)
        value = Value(properties, encoding=Encoding.PROPERTY)
        return self.ws.put(path, value, quorum=1)

    def get_frontends(self, yaks=MY_YAKS):
        s = '{}/{}/frontend/*'.format(Admin.PREFIX, yaks)
        kvs = self.ws.get(s)
        #return list(map((lambda e: return self.__extract_id_v(e)), kvs))
        return list(map(self.__extract_id_v, kvs))

    def get_frontend(self, feid, yaks=MY_YAKS):
        pass

    def remove_frontend(self, feid, yaks=MY_YAKS):
        return True

    def add_backend(self, beid, properties, yaks=MY_YAKS):
        return True

    def get_backends(self, yaks=MY_YAKS):
        pass

    def get_backend(self, beid, yaks=MY_YAKS):
        pass

    def remove_backend(self, beid, yaks=MY_YAKS):
        pass

    def add_storage(self, stid, properties, beid=None, yaks=MY_YAKS):
        return True

    def get_storages(self, beid=None, yaks=MY_YAKS):
        return []

    def get_storage(self, stid, yaks=MY_YAKS):
        pass

    def remove_storage(self, stid, yaks=MY_YAKS):
        pass

    def get_sessions(self, yaks=MY_YAKS, feid=None):
        return []

    def close_session(self, sid, yaks=MY_YAKS):
        pass

    def get_subscriptions(self, sid, yaks=MY_YAKS):
        pass
