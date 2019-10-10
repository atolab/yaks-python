import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

locator = 'tcp/127.0.0.1:7447'
if len(sys.argv) > 1 :
    locator = sys.argv[1]

# If not specified as 2nd argument, use a relative path (to the workspace below): 'yaks-java-put'
path = 'yaks-python-put'
if len(sys.argv) > 2 :
    path = sys.argv[2]

value = 'Put from Yaks Python!'
if len(sys.argv) > 3 :
    value = sys.argv[3]

print('Login to {}...'.format(locator))
y = Yaks.login(locator)

print('Use Workspace on "/demo/example"')
w = y.workspace('/demo/example')

print('Put on {} : {}'.format(path, value))
w.put(path, Value(value, encoding=Encoding.STRING))

y.logout()
