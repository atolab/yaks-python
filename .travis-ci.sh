#!/usr/bin/env bash

WD=$(pwd)
cd $(mktemp -d)
RD=$(pwd)
curl -L -o zenohd https://github.com/atolab/atobin/raw/master/zenoh/unstable/ubuntu/16.04/zenohd
curl -L -o yaks-plugin.cmxs https://github.com/atolab/atobin/tree/master/yaks/unstable/ubuntu/16.04/yaks-plugin.cmxs
chmod +x $RD/zenohd
$RD/zenohd -P "yaks-plugin.cmxs -w" --verbosity=debug > $RD/zenohd.out 2>&1 & echo $! > $RD/zenohd.pid
ZPID=$(<"$RD/zenohd.pid")
sleep 2;
cat $YD/zenohd.out
echo "ZENOHD PID $ZPID"
cd $WD
echo "Running tests from $WD"
tox
echo "KILLING ZENOHD $ZPID"
kill -15 $ZPID
rm -rf $RD
exit 0