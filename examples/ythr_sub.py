import time
import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value
import threading
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-z", "--zenoh", required=False,
                help="ip:port for the zenoh router")

args = vars(ap.parse_args())
zlocator = args['zenoh']

y = Yaks.login(zlocator)
ws = y.workspace('/')
N = 50000
count = 0
start = 0


def listener(kvs):
    for (k, v) in kvs:
        global count
        global start
        global N
        if count == 0:
            start = time.time()
            count += 1
        elif count < N:
            count += 1
        else:
            delta = time.time() - start
            count = 0
            thr = N / delta
            print("{} mgs/sec".format(thr))


path = '/ylatp/sample'
ws.subscribe(path, listener)

time.sleep(60)
