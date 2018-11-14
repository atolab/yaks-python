#!/usr/bin/env bash

WD=$(pwd)
cd $(mktemp -d)
YD=$(pwd)
curl -L -o yaks.tar.gz https://www.dropbox.com/s/275sm1vux7ywvy3/yaks.tar.gz
tar -xzvf yaks.tar.gz
$YD/yaksd -w > $YD/yaks.out 2>&1 & echo $! > $YD/yaks.pid
YPID=$(<"$YD/yaks.pid")
cat $YD/yaks.out
echo "YAKS PID $YPID"
cd $WD
echo "Running tests from $WD"
tox
echo "KILLING YAKS $YPID"
kill -15 $YPID
rm -rf $YD
exit 0