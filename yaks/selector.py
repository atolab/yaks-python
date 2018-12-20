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


class Selector(object):
    def __init__(self, selector):
        self.__sel_regex = re.compile(
            '^([^?#]+)(\?([^\[\]#]*)(\[(.*)\])?)?(\#(.*))?$')
        if not self.is_valid(selector):
            raise ValidationError(
                "{} is not a valid Selector".format(selector))
        res = self.__sel_regex.match(selector)
        self.selector = selector
        self.path = res.group(1)
        self.predicate = res.group(3)
        self.properties = res.group(5)
        self.fragment = res.group(7)

    def is_valid(self, selector):
        return self.__sel_regex.match(selector) is not None \
            and not selector.startswith('//')

    def is_absolute(self):
        if self.path.startswith('/'):
            return True
        return False

    def is_path_unique(self):
        return '*' not in self.path

    def is_prefixed_by_path(self, path):
        return self.path.startswith(path)

    def to_string(self):
        return self.selector

    def get_path(self):
        return self.path

    def get_predicate(self):
        return self.predicate

    def get_fragment(self):
        return self.fragment

    def get_properties(self):
        return self.properties

    def dict_from_properties(self):
        data = {}
        if self.properties is None:
            return data
        uri_values = self.properties.split(';')
        #print (uri_values)
        for tokens in uri_values:
            v = tokens.split('=')[-1]
            k = tokens.split('=')[0]
            if len(k.split('.')) < 2:
                data.update({k: v})
            else:
                d = self.__dot2dict(k, v)
                data.update(d)
        return data

    def __dot2dict(self, dot_notation, value=None):
        ld = []

        tokens = dot_notation.split('.')
        n_tokens = len(tokens)
        for i in range(n_tokens, 0, -1):
            if i == n_tokens and value is not None:
                ld.append({tokens[i - 1]: value})
            else:
                ld.append({tokens[i - 1]: ld[-1]})
        return ld[-1]

    def __len__(self):
        return len(self.selector)

    def __eq__(self, second_selector):
        if isinstance(second_selector, self.__class__):
            return self.selector == second_selector.selector
        return False

    def __str__(self):
        return self.selector

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.selector.__hash__()
