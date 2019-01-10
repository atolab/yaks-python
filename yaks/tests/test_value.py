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
from yaks import Value
from yaks.encoding import *


class ValueTests(unittest.TestCase):

    def test_raw_value(self):
        v = Value('test raw value')
        self.assertEqual('test raw value', v.get_value())
        self.assertEqual(Encoding.RAW, v.encoding)

    def test_string_value(self):
        v = Value('test string value', encoding=Encoding.STRING)
        self.assertEqual('test string value', v.get_value())
        self.assertEqual(Encoding.STRING, v.encoding)

    def test_json_value(self):
        d = {
            'this': 'is',
            'a': 'json value'
        }
        v = Value(d, encoding=Encoding.JSON)
        self.assertEqual(d, v.get_value())
        self.assertEqual(Encoding.JSON, v.encoding)

    def test_sql_value(self):
        sql = ['this', 'is', 'a', 'sql', 'value']
        v = Value(sql, encoding=Encoding.SQL)
        self.assertEqual(sql, v.get_value())
        self.assertEqual(Encoding.SQL, v.encoding)

    def test_pb_value(self):
        pb = 'some protobuf...'
        self.assertRaises(ValueError, Value, pb, Encoding.PROTOBUF)

    def test_unsupported_value(self):
        pb = 'some value...'
        self.assertRaises(ValueError, Value, pb, 0x100)
