import time
import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value
import threading

y = Yaks.login(sys.argv[1])
ws = y.workspace('/')
N = 20000
count = 0
start = 0


def listener(kvs):
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
