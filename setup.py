# Copyright (c) 2018 ADLINK Technology Inc.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the LGPL 2.1 which is available at
# https://github.com/atolab/yaks/blob/master/LICENSE
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - API

#!/usr/bin/env python3

from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='yaks',
    version='0.2.6',
    author='ADLINK Advance Technology Office',
    description='Python API to access the YAKS service',
    long_description=read('README.md'),
    packages=['yaks'],
    url='https://github.com/atolab/yaks-python',
    authon_email='gabriele.baldoni@adlinktech.com',
    install_requires=['hexdump', 'mvar', 'papero==0.2.6'],
    license='Apache 2.O or EPL 2.0',
    classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Telecommunications Industry',
          'License :: OSI Approved :: Apache Software License',
          'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)',
          'Programming Language :: Python :: 3',
        #   'Programming Language :: Python :: 2'
    ],
    include_package_data=True
)
