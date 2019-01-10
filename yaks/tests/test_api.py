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

from yaks import Yaks

from yaks import Selector
from yaks import Path
from yaks import Value
from yaks.exceptions import *
import time


class APITest(unittest.TestCase):

    def bogustest(self):
        self.assertTrue(True)

    # def test_create_close_api(self):
    #     #y = YAKS()
    #     #self.assertFalse(y.is_connected)
    #     y = Yaks.login('127.0.0.1')
    #     self.assertTrue(y.is_connected)
    #     y.logout()
    #     self.assertFalse(y.is_connected)

    # def test_create_delete_storage(self):
    #     y = Yaks.login('127.0.0.1')
    #     properties = {'is.yaks.storage.selector': Selector('/myyaks')}
    #     sid = y.create_storage('123', properties)
    #     self.assertEqual(sid, '123')
    #     y.remove_storage(sid)
    #     y.logout()

    # def test_create_delete_workspace(self):
    #     y = Yaks.login('127.0.0.1')
    #     properties = {'is.yaks.storage.selector': Selector('/myyaks')}
    #     sid = y.create_storage('123', properties)
    #     workspace = y.workspace('/myyaks')
    #     self.assertEqual(sid, '123')
    #     self.assertEqual(workspace.path, '/myyaks')
    #     workspace.dispose()
    #     y.remove_storage(sid)
    #     y.logout()

    # def test_put_get_remove(self):
    #     y = Yaks.login('127.0.0.1')
    #     properties = {'is.yaks.storage.selector': Selector('/myyaks')}
    #     sid = y.create_storage('123', properties)
    #     workspace = y.workspace('/myyaks')
    #     d = Value(json.dumps({'value': 1}))
    #     self.assertTrue(workspace.put('/myyaks/key1', d))
    #     nd = workspace.get('/myyaks/key1')[0]
    #     k, v = nd
    #     self.assertEqual(v, d)
    #     self.assertEqual(k, Path('/myyaks/key1'))
    #     d = Value(json.dumps({'value': 2}))
    #     self.assertTrue(workspace.remove('/myyaks/key1'))
    #     self.assertEqual(workspace.get(('/myyaks/key1'), [])
    #     workspace.dispose()
    #     y.remove_storage(sid)
    #     y.logout()

    # def test_sub_unsub(self):
    #     y=Yaks.login('127.0.0.1')
    #     properties={'is.yaks.storage.selector': Selector('/myyaks')}
    #     stid=y.create_storage('123', properties)
    #     workspace=y.workspace('/myyaks')
    #     local_var=mvar.MVar()

    #     def cb(kvs):
    #         self.assertEqual(kvs,
    #                          [(Path('/myyaks/key1'), Value('123'))]
    #         local_var.put(kvs)

    #     sid=workspace.subscribe('/myyaks/key1', cb)
    #     workspace.put('/myyaks/key1', Value('123'))
    #     self.assertEqual(local_var.get(),
    #                      [(Path('/myyaks/key1'), Value('123'))])
    #     self.assertTrue(workspace.unsubscribe(sid))
    #     workspace.dispose()
    #     y.remove_storage(stid)
    #     y.logout()

    # def test_eval(self):
    #     y=Yaks.login('127.0.0.1')
    #     properties={'is.yaks.storage.selector': Selector('/myyaks')}
    #     stid=y.create_storage('123', properties)
    #     workspace=y.workspace(Path('/myyaks'))

    #     def cb(path, hello):
    #         return Value('{} World!'.format(hello))

    #     workspace.eval(Path('/myyaks/key1'), cb)
    #     kvs=workspace.get('/myyaks/key1?[hello=mondo]')
    #     self.assertEqual(kvs,
    #                      [{'key': Path('/myyaks/key1'),
    #                           'value': Value('mondo World!')}])
    #     workspace.remove('/myyaks/key1')
    #     workspace.dispose()
    #     y.remove_storage(stid)
    #     y.logout()
