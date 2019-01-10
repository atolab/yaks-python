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

# Encoding

from enum import Enum

# TODO: This should be changed in enum


class Encoding(object):
    RAW = 0x01
    STRING = 0x02
    JSON = 0x03
    PROTOBUF = 0x04
    SQL = 0x05
    PROPERTY = 0x6
    # The following are both invalid encoding,
    # only numbers in this range are valid
    MIN = 0x00
    MAX = 0xff


class TranscodingFallback(Enum):
    FAIL = 0x01
    DROP = 0x02
    KEEP = 0x03
