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
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - Initial commit

# -*-Makefile-*-

WD := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))));

all:
	echo "Nothing to do";

install:
	python3 setup.py install --record yaks_files.txt


clean:
	rm -rf ./build ./dist ./yaks.egg-info;
	rm -rf yaks_api.log .tox yaks.egg-info ./yaks/__pycache__/ ./yaks/tests/__pycache__/;

test:
	tox
	
doc:	
	mkdir -p docs/html &>/dev/null
	pdoc --html --html-dir ./docs/html/ --all-submodules --overwrite yaks
