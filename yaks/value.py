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
from yaks.encoding import *


class Value(object):
    def __init__(self, value, encoding=RAW):
        if encoding > 0xFF:
            raise ValueError('Encoding not supported')
        self.encoding = encoding
        self.value = value

    def get_encoding(self):
        return self.encoding

    def get_value(self):
        return self.value

    def __eq__(self, second_value):
        if isinstance(second_value, self.__class__):
            return self.value == second_value.value
        return False

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
