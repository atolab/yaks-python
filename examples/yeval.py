import sys
import concurrent.futures
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value, Change, ChangeKind

locator = 'tcp/127.0.0.1:7447'
if len(sys.argv) > 1 :
    locator = sys.argv[1]

path = '/demo/example/yaks-java-eval'
if len(sys.argv) > 2 :
    path = sys.argv[2]

print('Login to {}...'.format(locator))
y = Yaks.login(locator)

print('Use Workspace on "/"')
# Note that we give a ThreadPool to the workspace here, for our eval_callback below
# to be called in a separate thread rather that in Yaks I/O thread.
# Thus, the callback can perform some Yaks operations (e.g.: get)
w = y.workspace('/', concurrent.futures.ThreadPoolExecutor())

def eval_callback(path, properties):
    # In this Eval function, we choosed to get the name to be returned in the StringValue in 3 possible ways,
    # depending the properties specified in the selector. For example, with the following selectors:
    #   - '/demo/example/yaks-java-eval' : no properties are set, a default value is used for the name
    #   - '/demo/example/yaks-java-eval?(name=Bob)' : 'Bob' is used for the name
    #   - '/demo/example/yaks-java-eval?(name=/demo/example/name)' :
    #     the Eval function does a GET on '/demo/example/name' an uses the 1st result for the name
    print('>> Processing eval for path {} with properties: {}'.format(path, properties))
    name = properties.get('name', 'Yaks Python!')

    if name.startswith('/'):
        print('   >> Get name to use from Yaks at path: {}'.format(name))
        kvs = w.get(name)
        if len(kvs) > 0:
            name = kvs[0][1]

    print('   >> Returning string: "Eval from {}"'.format(name))
    return Value('Eval from {}'.format(name), encoding=Encoding.STRING)


print('Register eval {}'.format(path))
w.register_eval(path, eval_callback)

print('Enter \'q\' to quit...')
while sys.stdin.read(1) != 'q': ()

w.unregister_eval(path)
y.logout()