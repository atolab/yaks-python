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
from yaks import message
from yaks import Selector
from yaks import Path
from yaks import Value
from yaks.encoding import *


class MessagesTests(unittest.TestCase):

    def bogustest(self):
        self.assertTrue(True)
    # def test_pack_unpack(self):
    #     msg1 = messages.Message()
    #     msg1.message_code = 0xFE
    #     msg1.generate_corr_id()

    #     cid = msg1.corr_id
    #     msg1.add_property('key1', 'value1')
    #     msg1.add_property('key2', 'value2')

    #     packed_msg1 = msg1.pack()

    #     msg2 = messages.Message(packed_msg1)

    #     self.assertEqual(cid, msg2.corr_id)
    #     self.assertEqual(msg1.message_code, msg2.message_code)
    #     self.assertEqual(msg1.flags, msg2.flags)
    #     self.assertEqual(msg1.properties, msg2.properties)
    #     self.assertEqual(msg2.get_property('key1'), 'value1')

    # def test_pack_for_tx(self):
    #     msg1 = messages.Message()
    #     msg1.message_code = 0xFE
    #     msg1.corr_id = 1
    #     packed_msg1 = msg1.pack_for_transport()
    #     data = b'\x03\xfe\x00\x01'

    #     self.assertEqual(data, packed_msg1)

    # def test_set_unset_flags(self):
    #     msg1 = messages.Message()
    #     msg1.set_a()
    #     msg1.set_p()
    #     msg1.set_s()
    #     msg2 = messages.Message(msg1.pack())

    #     self.assertEqual(msg2.flags, 7)
    #     msg2.unset_p()
    #     self.assertEqual(msg2.flags, 6)
    #     msg2.unset_s()
    #     self.assertEqual(msg2.flags, 4)
    #     msg2.unset_a()
    #     self.assertEqual(msg2.flags, 0)

    # def test_add_remove_property(self):
    #     msg1 = messages.Message()
    #     msg1.add_property('key1', 'value1')
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     msg2.remove_property('key1')
    #     self.assertEqual(msg2.properties, [])

    # def test_get_none_property(self):
    #     msg1 = messages.Message()
    #     self.assertEqual(msg1.get_property('key1'), None)

    # def test_add_get_string(self):
    #     msg1 = messages.Message()
    #     msg1.add_path(Path('/test_string_as_payload'))
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     self.assertEqual(Path('/test_string_as_payload'), msg2.get_path())

    # def test_add_get_values(self):
    #     msg1 = messages.Message()
    #     v1 = [
    #         {'key': Path('/hello'), 'value': Value('world')},
    #         {'key': Path('/another'), 'value': Value('longvalue')}
    #     ]
    #     msg1.message_code = messages.VALUES
    #     msg1.add_values(v1)
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     v2 = msg2.get_values()
    #     self.assertEqual(v1, v2)

    # def test_set_encoding_json(self):
    #     v1 = [
    #         {'key': Path('/hello'), 'value': Value('world', encoding=JSON)},
    #         {'key': Path('/another'),
    #                      'value': Value('longvalue', encoding=JSON)}
    #     ]
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.VALUES
    #     msg1.add_values(v1)
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     self.assertEqual(msg1.flags, msg2.flags)
    #     self.assertEqual(msg2.get_values(), v1)

    # def test_set_encoding_raw(self):
    #     v1 = [
    #         {'key': Path('/hello'), 'value': Value('world')},
    #         {'key': Path('/another'), 'value': Value('longvalue')}
    #     ]
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.VALUES
    #     msg1.add_values(v1)
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     self.assertEqual(msg1.flags, msg2.flags)
    #     self.assertEqual(msg2.get_values(), v1)

    # def test_set_encoding_string(self):
    #     v1 = [
    #      {'key': Path('/hello'), 'value': Value('world', encoding=STRING)},
    #      {'key': Path('/another'),
    #                      'value': Value('longvalue', encoding=STRING)}
    #     ]
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.VALUES
    #     msg1.add_values(v1)
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     self.assertEqual(msg1.flags, msg2.flags)
    #     self.assertEqual(msg2.get_values(), v1)

    # def test_set_encoding_sql(self):
    #     v1 = [
    #         {'key': Path('/sql'),
    #                      'value': Value((['val1', 'val2'], ['col1', 'col2']),
    #                                     encoding=SQL)}
    #     ]
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.VALUES
    #     msg1.add_values(v1)
    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)
    #     self.assertEqual(msg1.flags, msg2.flags)
    #     self.assertEqual(msg2.get_values(), v1)

    # def test_value_encoding_invalid(self):
    #     v1 = [
    #     {'key': Path('/hello'), 'value': Value('world', encoding=INVALID)},
    #     ]
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.VALUES
    #     self.assertRaises(ValueError, msg1.add_values, v1)

    # def test_value_encoding_unknown(self):
    #     v1 = [
    #         {'key': Path('/hello'), 'value': Value('world', encoding=0xFE)},
    #     ]
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.VALUES
    #     self.assertRaises(ValueError, msg1.add_values, v1)

    # def test_set_notification(self):
    #     v1 = [{'key': Path('hello'), 'value': Value('world')}]
    #     sid = '1234'
    #     msg1 = messages.Message()
    #     msg1.message_code = messages.NOTIFY
    #     msg1.add_notification(sid, v1)

    #     packed = msg1.pack()
    #     msg2 = messages.Message(packed)

    #     self.assertEqual(msg2.message_code, messages.NOTIFY)
    #     self.assertEqual(msg2.get_notification(), (sid, v1))

    # def test_ok_message(self):
    #     msg1 = messages.MessageOk('123')
    #     self.assertEqual(msg1.message_code, 0xD0)

    # def test_error_message(self):
    #     msg1 = messages.MessageError('123', 1234)

    #     self.assertEqual(msg1.message_code, 0xE0)
    #     self.assertEqual(1234, msg1.get_error())

    # def test_open_message(self):
    #     msg1 = messages.MessageOpen()
    #     self.assertEqual(msg1.message_code, 0x01)

    # def test_open_message_w_credentials(self):
    #     msg1 = messages.MessageOpen('usr', 'pwd')
    #     msg2 = messages.Message(msg1.pack())

    #     self.assertEqual(msg2.message_code, 0x01)
    #     self.assertEqual(msg1.get_property('yaks.login'), 'usr:pwd')

    # def test_create_access(self):
    #     msg1 = messages.MessageCreate(
    #         messages.EntityType.WORKSPACE, Path('/my/path'))
    #     self.assertEqual(msg1.message_code, 0x02)
    #     self.assertEqual(msg1.flag_a, 1)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_path(), Path('/my/path'))

    # def test_create_access_w_properties(self):
    #     properties = {
    #         'is.yaks.access.alias': 123,
    #         'is.yaks.access.cachesize': '1024'
    #     }
    #     msg1 = messages.MessageCreate(
    #         messages.EntityType.WORKSPACE, Path('/my/path'), properties)
    #     self.assertEqual(msg1.message_code, 0x02)
    #     self.assertEqual(msg1.flag_a, 1)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_path(), Path('/my/path'))

    # def test_create_storage(self):
    #     msg1 = messages.MessageCreate(
    #         messages.EntityType.STORAGE, Selector('/my/path'))
    #     self.assertEqual(msg1.message_code, 0x02)
    #     self.assertEqual(msg1.flag_s, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.get_selector(), Selector('/my/path'))

    # def test_create_storage_w_properties_n_config(self):
    #     config = {'backendip': '127.0.0.1', 'port': 8888}
    #     properties = {
    #         'is.yaks.storage.config': config,
    #         'is.yaks.storage.alias': 'store1'
    #     }
    #     msg1 = messages.MessageCreate(
    #         messages.EntityType.STORAGE, Selector('/my/path'), properties)
    #     self.assertEqual(msg1.message_code, 0x02)
    #     self.assertEqual(msg1.flag_s, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.get_selector(), Selector('/my/path'))

    # def test_delete_storage(self):
    #     msg1 = messages.MessageDelete('123', messages.EntityType.STORAGE)
    #     self.assertEqual(msg1.message_code, 0x03)
    #     self.assertEqual(msg1.flag_s, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_p, 1)

    # def test_delete_access(self):
    #     msg1 = messages.MessageDelete('321', messages.EntityType.WORKSPACE)
    #     self.assertEqual(msg1.message_code, 0x03)
    #     self.assertEqual(msg1.flag_a, 1)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.flag_p, 1)

    # def test_delete_value(self):
    #     msg1 = messages.MessageDelete('321', path=Path('/my/path'))
    #     self.assertEqual(msg1.message_code, 0x03)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_path(), Path('/my/path'))

    # def test_put_value(self):
    #     msg1 = messages.MessagePut('321', Path('/my/path'), Value('avalue'))
    #     v = [{'key': Path('/my/path'), 'value': Value('avalue')}]
    #     self.assertEqual(msg1.message_code, 0xA0)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_values(), v)

    # def test_patch_value(self):
    #     msg1 = messages.MessagePatch(
    #         '321', Path('/my/path'), Value('a_new_value'))
    #     v = [{'key': Path('/my/path'), 'value': Value('a_new_value')}]
    #     self.assertEqual(msg1.message_code, 0xA1)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_values(), v)

    # def test_get_value(self):
    #     msg1 = messages.MessageGet('321', Selector('/my/path'))
    #     self.assertEqual(msg1.message_code, 0xA2)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_selector(), Selector('/my/path'))

    # def test_value_message(self):
    #     v1 = [
    #         {'key': Path('/hello'), 'value': Value('world')},
    #     ]
    #     msg1 = messages.MessageValues('321', v1)
    #     self.assertEqual(msg1.message_code, 0xD1)
    #     self.assertEqual(msg1.flag_p, 0)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_values(), v1)
    #     self.assertEqual(msg1.corr_id, '321')

    # def test_subscribe_message(self):
    #     msg1 = messages.MessageSub('321', Selector('/my/path'))
    #     self.assertEqual(msg1.message_code, 0xB0)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_subscription(), Selector('/my/path'))

    # def test_unsubscribe_message(self):
    #     msg1 = messages.MessageUnsub('321', '121241')
    #     self.assertEqual(msg1.message_code, 0xB1)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_subscription_id(), '121241')

    # def test_eval_message(self):
    #     msg1 = messages.MessageEval('321', Path('/my/path'))
    #     self.assertEqual(msg1.message_code, 0xB3)
    #     self.assertEqual(msg1.flag_p, 1)
    #     self.assertEqual(msg1.flag_a, 0)
    #     self.assertEqual(msg1.flag_s, 0)
    #     self.assertEqual(msg1.get_path(), Path('/my/path'))
