from yaks import Yaks, Value, Encoding, Change, ChangeKind
import signal

p='/f0rce/6214b769-21e1-4c8e-bdd8-dc90943bf1ec/leave'
p2='/f0rce/6214b769-21e1-4c8e-bdd8-dc90943bf1ec/gone'
v = Value('this is a test value',encoding=Encoding.STRING)
y = Yaks.login('')
ws = y.workspace('/')


def obs(kcs):
    for kc in kcs:
        k = kc[0]
        c = kc[1]
        if c.get_kind() == ChangeKind.PUT:
            v2 = Value('we have to leave', encoding=Encoding.STRING)
            ws.put(p2, v2)
        elif c.get_kind() == ChangeKind.REMOVE:
            ws.remove(p2)
        else:
            print('Unknown kind')

def obs2(kcs):
    for kc in kcs:
        k = kc[0]
        c = kc[1]
        if c.get_kind() == ChangeKind.PUT:
            print(c)
        elif c.get_kind() == ChangeKind.REMOVE:
            print("remove for {}".format(k))
        else:
            print('Unknown kind')


ws.subscribe(p,obs)
ws.subscribe(p2,obs2)


for _ in range(1, 10000):
    ws.put(p,v)

