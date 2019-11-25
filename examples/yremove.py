import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

# If not specified as 1st argument, use a relative path
# (to the workspace below): 'yaks-python-put'
path = 'yaks-python-put'
if len(sys.argv) > 1:
    path = sys.argv[1]

locator = None
if len(sys.argv) > 2:
    locator = sys.argv[2]

print('Login to Yaks (locator={})...'.format(locator))
y = Yaks.login(locator)

print('Use Workspace on "/demo/example"')
w = y.workspace('/demo/example')

print('Remove {}'.format(path))
w.remove(path)

y.logout()
