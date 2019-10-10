import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

locator = 'tcp/127.0.0.1:7447'
if len(sys.argv) > 1:
    locator = sys.argv[1]

selector = '/demo/example/**'
if len(sys.argv) > 2:
    selector = sys.argv[2]

print('Login to {}...'.format(locator))
y = Yaks.login(locator)

print('Use Workspace on "/"')
w = y.workspace('/')

print('Get from {}'.format(selector))
for (k, v) in w.get(selector):
    print('  {} : {}'.format(k, v))


y.logout()
