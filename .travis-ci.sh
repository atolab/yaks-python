#!/usr/bin/env bash

WD=$(pwd)
cd $(mktemp -d)
YD=$(pwd)
# curl -L -o /usr/local/lib/libzenohc.so https://github.com/atolab/atobin/raw/master/zenoh-c/latest/ubuntu/16.04/libzenohc.so
curl -L -o yaksd https://github.com/atolab/atobin/raw/master/yaks/latest/ubuntu/16.04/yaksd
# tar -xzvf yaks.tar.gz
chmod +x $YD/yaksd
$YD/yaksd -w -z "zenohd" --verbosity=debug > $YD/yaks.out 2>&1 & echo $! > $YD/yaks.pid
YPID=$(<"$YD/yaks.pid")
sleep 2;
cat $YD/yaks.out
echo "YAKS PID $YPID"
cd $WD
echo "Running tests from $WD"
tox
echo "KILLING YAKS $YPID"
kill -15 $YPID
rm -rf $YD
exit 0