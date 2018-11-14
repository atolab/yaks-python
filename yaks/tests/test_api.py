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
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - Tests

import unittest
import json
from yaks import mvar
from yaks import YAKS


class APITest(unittest.TestCase):

    def test_create_close_api(self):
        # y = YAKS(server_address='127.0.0.1')
        # self.assertTrue(y.is_connected)
        # y.close()
        self.assertTrue(True)

    def test_create_delete_storage(self):
        # y = YAKS(server_address='127.0.0.1')
        # storage = y.create_storage('//yaks')
        # self.assertEqual(storage.path, '//yaks')
        # storage.dispose()
        # y.close()
        self.assertTrue(True)

    def test_create_delete_access(self):
        # y = YAKS(server_address='127.0.0.1')
        # storage = y.create_storage('//yaks')
        # access = y.create_access('//yaks')
        # self.assertEqual(storage.path, '//yaks')
        # self.assertEqual(access.path, '//yaks')
        # access.dispose()
        # storage.dispose()
        # y.close()
        self.assertTrue(True)

    def test_put_get_remove(self):
        # y = YAKS(server_address='127.0.0.1')
        # storage = y.create_storage('//yaks')
        # access = y.create_access('//yaks')
        # d = json.dumps({'value': 1})
        # self.assertTrue(access.put('//yaks/key1', d))
        # nd = access.get('//yaks/key1')[0]
        # k = nd.get('key')
        # v = nd.get('value')
        # self.assertEqual(v, d)
        # self.assertEqual(k, '//yaks/key1')
        # d = json.dumps({'value': 2})
        # self.assertTrue(access.remove('//yaks/key1'))
        # self.assertEqual(access.get('//yaks/key1'), [])
        # access.dispose()
        # storage.dispose()
        # y.close()
        self.assertTrue(True)

    def test_sub_unsub(self):
        # y = YAKS(server_address='127.0.0.1')
        # storage = y.create_storage('//yaks')
        # access = y.create_access('//yaks')
        # local_var = mvar.MVar()

        # def cb(kvs):
        #     local_var.put(kvs)

        # sid = access.subscribe('//yaks/key1', cb)
        # access.put('//yaks/key1', '123')
        # self.assertEqual(local_var.get(),
        #                  [{'key': '//yaks/key1', 'value': '123'}])
        # self.assertTrue(access.unsubscribe(sid))
        # access.dispose()
        # storage.dispose()
        # y.close()
        self.assertTrue(True)
