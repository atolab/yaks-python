import time
import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

y = Yaks.login(sys.argv[1])
ws = y.workspace('/')
samples = int(sys.argv[2])

start = time.time()
path = '/ylatp/sample'
for i in range(0, samples):
    ws.z_put(path, Value('01234567', Encoding.STRING))
stop = time.time()
delta = stop - start

print("Sent {} samples in {}".format(samples, delta))
print("Throughput: {} msg/sec".format(samples / delta))
print("Average : {}".format(delta / samples))
