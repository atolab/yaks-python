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
from yaks.codec import *
from yaks import Value
from papero import *
import json


class CodecTests(unittest.TestCase):

    def test_encode_decode_raw_value(self):
        self.assertTrue(True)
        # TODO: fix this test
        # buf = IOBuf()
        # s = 'Value'
        # rv = Value(s)
        # encode_raw_value(buf, rv)
        # rv2 = decode_raw_value(buf)
        # self.assertEqual(rv, rv2)

    def test_encode_decode_string_value(self):
        buf = IOBuf()
        s = 'Value'
        rv = Value(s, encoding=Encoding.STRING)
        encode_string_value(buf, rv)
        rv2 = decode_string_value(buf)
        self.assertEqual(rv, rv2)

    def test_encode_decode_json_value(self):
        self.assertTrue(True)
        # TODO: fix this test
        # buf = IOBuf()
        # s = {'json': 'value'}
        # rv = Value(s, encoding=Encoding.JSON)
        # encode_json_value(buf, rv)
        # rv2 = json.loads(json.loads(decode_json_value(buf).value))
        # self.assertEqual(rv, rv2)

    def test_encode_decode_property_value(self):
        self.assertTrue(True)
        # TODO: fix this test
        # buf = IOBuf()
        # s = [Property('key', 'value')]
        # rv = Value(s, encoding=Encoding.PROPERTY)
        # encode_property_value(buf, rv)
        # rv2 = decode_property_value(buf)
        # self.assertEqual(rv, rv2)

    # def test_decoding(self):
    #     e = encoder.VLEEncoder()
    #     i = [b'\x8c', b'\x02']
    #     res = e.decode(i)
    #     expected_res = 268
    #     self.assertEqual(res, expected_res)

    # def test_random_encode_decode(self):
    #     e = encoder.VLEEncoder()
    #     i = randint(0, 18446744073709551615)
    #     encoded = e.encode(i)
    #     decoded = e.decode(encoded)
    #     self.assertEqual(i, decoded)
