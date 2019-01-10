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
from yaks.message import *
from yaks import Selector
from yaks import Path
from yaks import Value
from yaks.encoding import *


class MessagesTests(unittest.TestCase):

    def test_message(self):
        m = Message(123)
        self.assertEqual(m.mid, 123)

    def test_header(self):
        p = [('pkey', 'pvalue')]
        h = Header(Message.OK, 0, p)
        h2 = Header(Message.LOGIN, 0)
        self.assertTrue(Header.has_flag(h.flags, Header.P_FLAG))
        self.assertEqual(h.corr_id, 0)
        self.assertEqual(h.properties, p)
        self.assertEqual(h.mid, Message.OK)

        self.assertFalse(Header.has_flag(h2.flags, Header.P_FLAG))
        self.assertEqual(h2.corr_id, 0)
        self.assertEqual(h2.properties, None)
        self.assertEqual(h2.mid, Message.LOGIN)
        self.assertFalse(h2.has_properties())

    def test_login(self):
        lm = LoginM()
        self.assertEqual(lm.mid, Message.LOGIN)

    def test_logout(self):
        lom = LogoutM()
        self.assertEqual(lom.mid, Message.LOGOUT)

    def test_workspacem(self):
        p = Path('/yaks')
        wm = WorkspaceM(p)
        self.assertEqual(wm.mid, Message.WORKSPACE)
        self.assertEqual(wm.path, Path('/yaks'))

    def test_workspace_message(self):
        wsid = '123'
        wsm = WorkspaceMessage(Message.PUT, wsid)
        self.assertEqual(wsm.mid, Message.PUT)
        self.assertEqual(wsm.wsid, wsid)
        self.assertEqual(wsm.properties, [Property('wsid', wsid)])

    def test_put(self):
        kvs = [(Path('/yaks/1'), Value('1234'))]
        wsid = '1'
        pm = PutM(wsid, kvs)
        self.assertEqual(pm.mid, Message.PUT)
        self.assertEqual(pm.wsid, wsid)
        self.assertEquals(pm.kvs, kvs)

    def test_get(self):
        s = Selector('/yaks/**')
        wsid = '123'
        gm = GetM(wsid, s)
        self.assertEqual(gm.mid, Message.GET)
        self.assertEqual(gm.wsid, wsid)
        self.assertEqual(gm.selector, s)

    def test_update(self):
        kvs = [(Path('/yaks/2'), Value('1235'))]
        wsid = '1'
        um = UpdateM(wsid, kvs)
        self.assertEqual(um.mid, Message.UPDATE)
        self.assertEqual(um.wsid, wsid)
        self.assertEquals(um.kvs, kvs)

    def test_delete(self):
        p = Path('/yaks/123')
        wsid = '123'
        dm = DeleteM(wsid, p)
        self.assertEqual(dm.mid, Message.DELETE)
        self.assertEqual(dm.wsid, wsid)
        self.assertEqual(dm.path, p)

    def test_subscribe(self):
        s = Selector('/yaks/**')
        wsid = '123'
        sm = SubscribeM(wsid, s)
        self.assertEqual(sm.mid, Message.SUB)
        self.assertEqual(sm.wsid, wsid)
        self.assertEqual(sm.selector, s)

    def test_unsubscribe(self):
        wsid = '123'
        subid = '456'
        usm = UnsubscribeM(wsid, subid)
        self.assertEqual(usm.mid, Message.UNSUB)
        self.assertEqual(usm.wsid, wsid)
        self.assertEqual(usm.subid, subid)

    def test_notify(self):
        wsid = '123'
        subid = '456'
        kvs = [(Path('/yaks/2'), Value('1235'))]
        nm = NotifyM(wsid, subid, kvs)
        self.assertEqual(nm.mid, Message.NOTIFY)
        self.assertEqual(nm.wsid, wsid)
        self.assertEqual(nm.subid, subid)
        self.assertEquals(nm.kvs, kvs)

    def test_eval(self):
        s = Selector('/yaks/**')
        wsid = '123'
        em = EvalM(wsid, s)
        self.assertEqual(em.mid, Message.EVAL)
        self.assertEqual(em.wsid, wsid)
        self.assertEqual(em.selector, s)

    def test_register_eval(self):
        p = Path('/yaks/eval')
        wsid = '1'
        msg = RegisterEvalM(wsid, p)
        self.assertEqual(msg.mid, Message.REG_EVAL)
        self.assertEqual(msg.wsid, wsid)
        self.assertEqual(msg.path, Path('/yaks/eval'))

    def test_unregister_eval(self):
        p = Path('/yaks/eval')
        wsid = '1'
        msg = UnregisterEvalM(wsid, p)
        self.assertEqual(msg.mid, Message.UNREG_EVAL)
        self.assertEqual(msg.wsid, wsid)
        self.assertEqual(msg.path, Path('/yaks/eval'))

    def test_values(self):
        kvs = [(Path('/yaks/1'), Value('1234'))]
        msg = ValuesM(kvs)
        h = Header(0, '123')
        msg2 = ValuesM.make(h, kvs)
        self.assertEqual(msg.mid, Message.VALUES)
        self.assertEquals(msg.kvs, kvs)
        self.assertEqual(msg2.mid, Message.VALUES)
        self.assertEquals(msg2.kvs, kvs)
        self.assertEquals(msg2.corr_id, '123')

    def test_ok(self):
        h = Header(0, '123', [Property('a', 'b')])
        msg = OkM.make(h)
        self.assertEqual(msg.mid, Message.OK)
        self.assertEquals(msg.properties, [Property('a', 'b')])
        self.assertEquals(msg.corr_id, '123')

    def test_error(self):
        msg = ErrorM.make('123', 100, [Property('a', 'b')])
        self.assertEqual(msg.mid, Message.ERROR)
        self.assertEqual(msg.error_code, 100)
        self.assertEquals(msg.properties, [Property('a', 'b')])
        self.assertEquals(msg.corr_id, '123')
