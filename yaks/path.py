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


def check(path):
    validate_selector_path(path)
    if path.startswith('//'):
        return False
    return True


def is_absolute(path):
    if path.startswith('/'):
        return True
    return False


def validate_selector_path(p):
    not_valid_chars = set('*?#')
    if any((c in not_valid_chars) for c in p):
        return False
    else:
        return True


def is_valid_selector(path):
    if path.startswith('//'):
        return False
    return True


def dot2dict(dot_notation, value=None):
    ld = []
    tokens = dot_notation.split('.')
    n_tokens = len(tokens)
    for i in range(n_tokens, 0, -1):
        if i == n_tokens and value is not None:
            ld.append({tokens[i - 1]: value})
        else:
            ld.append({tokens[i - 1]: ld[-1]})
    return ld[-1]


def args2dict(values):
    data = {}
    uri_values = values.split('&')
    for tokens in uri_values:
        v = tokens.split('=')[-1]
        k = tokens.split('=')[0]
        if len(k.split('.')) < 2:
            data.update({k: v})
        else:
            d = dot2dict(k, v)
            data.update(d)
    return data


def is_prefix(path, prefix):
    return path.startswith(prefix)


def get_query(path):
    q = path.split('?')[-1]
    return args2dict(q)
