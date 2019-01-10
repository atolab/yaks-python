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
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - Yaks API

import re
from yaks.exceptions import ValidationError
from yaks.encoding import Encoding
import json


class Value(object):
    def __init__(self, value, encoding=Encoding.RAW, raw_format=""):
        if encoding > Encoding.MAX:
            raise ValueError('Encoding not supported')
        if encoding == Encoding.PROTOBUF:
            raise ValueError('PROTOBUF Encoding not implemented')
        self.encoding = encoding
        if self.encoding == Encoding.JSON:
            if not (isinstance(value, dict) or isinstance(value, str)):
                raise ValidationError("Value is not a valid JSON")
            self.value = json.dumps(value)
        else:
            self.value = value
            self.raw_format = raw_format

    def get_encoding(self):
        return self.encoding

    def get_value(self):
        if self.encoding is Encoding.JSON:
            return json.loads(self.value)
        return self.value

    def __eq__(self, second_value):
        if isinstance(second_value, self.__class__):
            return self.value == second_value.value
        return False

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
