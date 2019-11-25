import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

# If not specified as 1st argument, use a relative path
# (to the workspace below): 'yaks-python-put'
path = 'yaks-python-put'
if len(sys.argv) > 1:
    path = sys.argv[1]

value = 'Put from Yaks Python!'
if len(sys.argv) > 2:
    value = sys.argv[2]

locator = None
if len(sys.argv) > 3:
    locator = sys.argv[3]

print('Login to Yaks (locator={})...'.format(locator))
y = Yaks.login(locator)

print('Use Workspace on "/demo/example"')
w = y.workspace('/demo/example')

print('Put on {} : {}'.format(path, value))
w.put(path, Value(value, encoding=Encoding.STRING))

y.logout()
