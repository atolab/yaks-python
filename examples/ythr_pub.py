import time
import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-z", "--zenoh", required=False,
                help="ip:port for the Zenoh router")

ap.add_argument("-s", "--samples", required=True,
                help="Samples to be sent as part of the test")

args = vars(ap.parse_args())
zlocator = args['zenoh']

samples = int(args['samples'])

y = Yaks.login(zlocator)
ws = y.workspace('/')


start = time.time()
path = '/ylatp/sample'
for i in range(0, samples):
    ws.put(path, Value('01234567', Encoding.STRING))
stop = time.time()
delta = stop - start

print("Sent {} samples in {}".format(samples, delta))
print("Throughput: {} msg/sec".format(samples / delta))
print("Average : {}".format(delta / samples))
