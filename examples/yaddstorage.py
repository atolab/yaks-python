import sys
from yaks import Yaks, Selector, Path, Workspace, Encoding, Value

locator = 'tcp/127.0.0.1:7447'
if len(sys.argv) > 1 :
    locator = sys.argv[1]

selector = '/demo/example/**'
if len(sys.argv) > 2 :
    selector = sys.argv[2]

storage_id = 'Demo'
if len(sys.argv) > 3 :
    storage_id = sys.argv[3]

print('Login to {}...'.format(locator))
y = Yaks.login(locator)

a = y.admin()

print('Add storage {} with selector {}'.format(storage_id, selector))
properties = {'selector': selector}
a.add_storage(storage_id, properties)

y.logout()
