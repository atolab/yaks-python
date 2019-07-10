import cProfile
import time
import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

y = Yaks.login(sys.argv[1])
ws = y.workspace('/')
samples = int(sys.argv[2])

res = time.clock_getres(time.CLOCK_REALTIME)
start = time.clock_gettime(time.CLOCK_REALTIME)
path = '/ylatp/sample'
for i in range(0, samples):
    ws.put(path + i, Value('01234567', Encoding.STRING))
stop = time.clock_gettime(time.CLOCK_REALTIME)
delta = stop - start

print("Sent {} samples in {}".format(samples, delta))
print("Throughput: {} msg/sec".format(samples / delta))
print("Average : {}".format(delta / samples))
