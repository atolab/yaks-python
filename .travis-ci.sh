#!/usr/bin/env bash

WD=$(PWD)
cd $(mktemp -d)
YD=$(PWD)
wget https://www.dropbox.com/s/jcm87oa8w65hv42/yaks.zip -O yaks.zip
unzip yaks.zip
$YD/yaksd -w > yaks.out 2>&1 & echo $! > $YD/yaks.pid
YPID=$(<"$YD/yaks.pid")
echo "YAKS PID $YPID"
cd $WD
echo "Running tests from $WD"
tox
echo "KILLING YAKS $YPID"
kill -15 $YPID