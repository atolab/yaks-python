import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

locator = None
if len(sys.argv) > 1:
    locator = sys.argv[1]

selector = '/demo/example/**'
if len(sys.argv) > 2:
    selector = sys.argv[2]

print('Login to Yaks (locator={})...'.format(locator))
y = Yaks.login(locator)

print('Use Workspace on "/"')
w = y.workspace('/')

print('Get from {}'.format(selector))
for entry in w.get(selector):
    print('  {} : {}'.format(entry.path, entry.value))


y.logout()
