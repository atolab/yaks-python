[![PyPI version](https://badge.fury.io/py/yaks.svg)](https://badge.fury.io/py/yaks)
[![Build Status](https://travis-ci.com/atolab/yaks-python.svg?token=LBmcudV28U4KHP4F42om&branch=master)](https://travis-ci.com/atolab/yaks-python)
[![codecov](https://codecov.io/gh/atolab/yaks-python/branch/master/graph/badge.svg)](https://codecov.io/gh/atolab/yaks-python)

# YAKS Python API v0.2

This repo contains the YAKS API binding for Python


#### Installation

    $ make install

or

    $ pip3 install yaks

To uninstall old versions run this until pip says there are no more packages

    $ pip3 uninstall yaks

#### Changelog

See [changelog file](CHANGELOG.md)

#### Examples

In the example folder you can find two examples, one uses main memory as storage for the data
while the other is using MariaDB.

In order to run the examples you need a YAKS Server running.

MainMemory Example:

    yaksd -w [--verbosity=debug]

Client:
    python3 client.py <yaks-ip>


You can also use the DB example with uses mariadb for storing data.

MariaDB Example:

You need a database demo and a table test.

Database Creation:

    # mysql -u root -p
    > create database demo;
    > use demo;

Define The tabla and put some test data:

    > CREATE TABLE test (id SERIAL NOT NULL PRIMARY KEY, mystring VARCHAR(255), myint INT, myfloat REAL, mydate DATE);
    > INSERT INTO test VALUES (1, 'test1', 1, 1.1, '2018-01-01');
    > INSERT INTO test VALUES (2, 'test2', 2, 2.2, '2018-02-02');
    > INSERT INTO test VALUES (3, 'test3', 3, 3.3, '2018-03-03');

Starting YAKS Server:

    yaksd [--verbosity=debug] -u mariadb://root:password@127.0.0.1:3306/test -w

Client:
    python3 client-sql.py <yasks-ip>


#### Docs

To generate html documentation you need **sphinx** and **sphinx_rtd_theme**

    $ pip3 install sphinx sphinx_rtd_theme
    $ make doc

The documentation can be find in two forms, pdf and html respectively under
- docs/build/latex/yaks.pdf
- docs/build/dirhtml/index.html


Copyright 2018 ADLINK Technology Inc.
