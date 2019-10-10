import sys
from yaks import Yaks, Selector, Path, Workspace
from yaks import Change, ChangeKind, Encoding, Value


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


def listener(changes):
    for (path, change) in changes:
        if change.get_kind() == ChangeKind.PUT:
            print('>> [Subscription listener] Received PUT on "{}": "{}"'
                  .format(path, change.get_value()))
        elif change.get_kind() == ChangeKind.UPDATE:
            print('>> [Subscription listener] Received UPDATE on "{}": "{}"'
                  .format(path, change.get_value()))
        elif change.get_kind() == ChangeKind.REMOVE:
            print('>> [Subscription listener] Received REMOVE on "{}"'
                  .format(path))
        else:
            print('>> [Subscription listener] Received kind:"{}" on "{}"'
                  .format(change.get_kind(), path))


print('Subscribe on {}'.format(selector))
subid = w.subscribe(selector, listener)

print('Enter \'q\' to quit...')
while sys.stdin.read(1) != 'q':
    pass

w.unsubscribe(subid)
y.logout()
