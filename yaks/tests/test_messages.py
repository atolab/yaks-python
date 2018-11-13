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
from yaks import messages


class MessagesTests(unittest.TestCase):
    def test_pack_unpack(self):
        msg1 = messages.Message()
        msg1.message_code = 0xFE
        msg1.generate_corr_id()

        cid = msg1.corr_id
        msg1.add_property('key1', 'value1')
        msg1.add_property('key2', 'value2')

        packed_msg1 = msg1.pack()

        msg2 = messages.Message(packed_msg1)

        self.assertEqual(cid, msg2.corr_id)
        self.assertEqual(msg1.message_code, msg2.message_code)
        self.assertEqual(msg1.flags, msg2.flags)
        self.assertEqual(msg1.properties, msg2.properties)
        self.assertEqual(msg2.get_property('key1'), 'value1')

    def test_pack_for_tx(self):
        msg1 = messages.Message()
        msg1.message_code = 0xFE
        msg1.corr_id = 1
        packed_msg1 = msg1.pack_for_transport()
        data = b'\x03\xfe\x00\x01'

        self.assertEqual(data, packed_msg1)

    def test_set_encoding(self):
        msg1 = messages.Message()
        msg1.set_encoding(messages.JSON)
        self.assertEqual(msg1.get_encoding(), messages.JSON)

    def test_add_remove_property(self):
        msg1 = messages.Message()
        msg1.add_property('key1', 'value1')
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        msg2.remove_property('key1')
        self.assertEqual(msg2.properties, [])

    def test_add_get_string(self):
        msg1 = messages.Message()
        msg1.add_path('test_string_as_payload')
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        self.assertEqual('test_string_as_payload', msg2.get_path())

    def test_add_get_values(self):
        msg1 = messages.Message()
        v1 = [
            {'key': 'hello', 'value': 'world'},
            {'key': 'another', 'value': 'longvalue'}
        ]
        msg1.set_encoding(messages.RAW)
        msg1.message_code = messages.VALUES
        msg1.add_values(v1)
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        v2 = msg2.get_values()
        self.assertEqual(v1, v2)

    def test_set_encoding_json(self):
        v1 = [
            {'key': 'hello', 'value': 'world'},
            {'key': 'another', 'value': 'longvalue'}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(messages.JSON)
        msg1.add_values(v1)
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        self.assertEqual(msg1.get_encoding(), msg2.get_encoding())
        self.assertEqual(msg1.flags, msg2.flags)
        self.assertEqual(msg2.get_values(), v1)

    def test_set_encoding_raw(self):
        v1 = [
            {'key': 'hello', 'value': 'world'},
            {'key': 'another', 'value': 'longvalue'}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(messages.RAW)
        msg1.add_values(v1)
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        self.assertEqual(msg1.get_encoding(), msg2.get_encoding())
        self.assertEqual(msg1.flags, msg2.flags)
        self.assertEqual(msg2.get_values(), v1)

    def test_set_encoding_string(self):
        v1 = [
            {'key': 'hello', 'value': 'world'},
            {'key': 'another', 'value': 'longvalue'}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(messages.STRING)
        msg1.add_values(v1)
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        self.assertEqual(msg1.get_encoding(), msg2.get_encoding())
        self.assertEqual(msg1.flags, msg2.flags)
        self.assertEqual(msg2.get_values(), v1)

    def test_set_encoding_sql(self):
        v1 = [
            {'key': 'hello', 'value': (['val1', 'val2'], ['col1', 'col2'])}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(messages.SQL)
        msg1.add_values(v1)
        packed = msg1.pack()
        msg2 = messages.Message(packed)
        self.assertEqual(msg1.get_encoding(), msg2.get_encoding())
        self.assertEqual(msg1.flags, msg2.flags)
        self.assertEqual(msg2.get_values(), v1)

    def test_set_encoding_protobuf(self):
        v1 = [
            {'key': 'hello', 'value': (['val1', 'val2'], ['col1', 'col2'])}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(messages.PROTOBUF)
        self.assertRaises(NotImplementedError, msg1.add_values, v1)

    def test_value_encoding_invalid(self):
        v1 = [
            {'key': 'hello', 'value': (['val1', 'val2'], ['col1', 'col2'])}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(messages.INVALID)
        self.assertRaises(ValueError, msg1.add_values, v1)

    def test_value_encoding_unknown(self):
        v1 = [
            {'key': 'hello', 'value': (['val1', 'val2'], ['col1', 'col2'])}
        ]
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        msg1.set_encoding(0xFE)
        self.assertRaises(ValueError, msg1.add_values, v1)

    def test_set_encoding_exception(self):
        msg1 = messages.Message()
        msg1.message_code = messages.VALUES
        self.assertRaises(ValueError, msg1.set_encoding, 0x100)

    def test_set_notification(self):
        v1 = [{'key': 'hello', 'value': 'world'}]
        sid = ['1234']
        msg1 = messages.Message()
        msg1.set_encoding(messages.STRING)
        msg1.message_code = messages.NOTIFY
        msg1.add_notification(sid, v1)

        packed = msg1.pack()
        msg2 = messages.Message(packed)

        self.assertEqual(msg2.message_code, messages.NOTIFY)
        self.assertEqual(msg2.get_notification(), (sid, v1))

    def test_ok_message(self):
        msg1 = messages.MessageOk('123')
        self.assertEqual(msg1.message_code, 0xD0)

    def test_error_message(self):
        msg1 = messages.MessageError('123', 1234)

        self.assertEqual(msg1.message_code, 0xE0)
        self.assertEqual(1234, msg1.get_error())

    def test_open_message(self):
        msg1 = messages.MessageOpen()
        self.assertEqual(msg1.message_code, 0x01)

    def test_open_message_w_credentials(self):
        msg1 = messages.MessageOpen('usr', 'pwd')
        msg2 = messages.Message(msg1.pack())

        self.assertEqual(msg2.message_code, 0x01)
        self.assertEqual(msg1.get_property('yaks.login'), 'usr:pwd')

    def test_create_access(self):
        msg1 = messages.MessageCreate(messages.EntityType.ACCESS, '//a/path')
        self.assertEqual(msg1.message_code, 0x02)
        self.assertEqual(msg1.flag_a, 1)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_path(), '//a/path')

    def test_create_access_w_properties(self):
        properties = {
            'is.yaks.access.alias': 123,
            'is.yaks.access.cachesize': '1024'
        }
        msg1 = messages.MessageCreate(
            messages.EntityType.ACCESS, '//a/path', properties)
        self.assertEqual(msg1.message_code, 0x02)
        self.assertEqual(msg1.flag_a, 1)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_path(), '//a/path')

    def test_create_storage(self):
        msg1 = messages.MessageCreate(messages.EntityType.STORAGE, '//a/path')
        self.assertEqual(msg1.message_code, 0x02)
        self.assertEqual(msg1.flag_s, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.get_path(), '//a/path')

    def test_create_storage_w_properties_n_config(self):
        config = {'backendip': '127.0.0.1', 'port': 8888}
        properties = {
            'is.yaks.storage.config': config,
            'is.yaks.storage.alias': 'store1'
        }
        msg1 = messages.MessageCreate(
            messages.EntityType.STORAGE, '//a/path', properties)
        self.assertEqual(msg1.message_code, 0x02)
        self.assertEqual(msg1.flag_s, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.get_path(), '//a/path')

    def test_delete_storage(self):
        msg1 = messages.MessageDelete('123', messages.EntityType.STORAGE)
        self.assertEqual(msg1.message_code, 0x03)
        self.assertEqual(msg1.flag_s, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_p, 1)

    def test_delete_access(self):
        msg1 = messages.MessageDelete('321', messages.EntityType.ACCESS)
        self.assertEqual(msg1.message_code, 0x03)
        self.assertEqual(msg1.flag_a, 1)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.flag_p, 1)

    def test_delete_value(self):
        msg1 = messages.MessageDelete('321', path='//a/path')
        self.assertEqual(msg1.message_code, 0x03)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_path(), '//a/path')

    def test_put_value(self):
        msg1 = messages.MessagePut('321', '//a/path', 'avalue')
        v = [{'key': '//a/path', 'value': 'avalue'}]
        self.assertEqual(msg1.message_code, 0xA0)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_values(), v)

    def test_patch_value(self):
        msg1 = messages.MessagePatch('321', '//a/path', 'a_new_value')
        v = [{'key': '//a/path', 'value': 'a_new_value'}]
        self.assertEqual(msg1.message_code, 0xA1)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_values(), v)

    def test_get_value(self):
        msg1 = messages.MessageGet('321', '//a/path')
        self.assertEqual(msg1.message_code, 0xA2)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_selector(), '//a/path')

    def test_value_message(self):
        v1 = [
            {'key': 'hello', 'value': 'world'},
        ]
        msg1 = messages.MessageValues('321', v1)
        self.assertEqual(msg1.message_code, 0xD1)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_values(), v1)

    def test_subscribe_message(self):
        msg1 = messages.MessageSub('321', '//a/path')
        self.assertEqual(msg1.message_code, 0xB0)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_subscription(), '//a/path')

    def test_unsubscribe_message(self):
        msg1 = messages.MessageUnsub('321', '121241')
        self.assertEqual(msg1.message_code, 0xB1)
        self.assertEqual(msg1.flag_p, 1)
        self.assertEqual(msg1.flag_a, 0)
        self.assertEqual(msg1.flag_s, 0)
        self.assertEqual(msg1.get_subscription(), '121241')
