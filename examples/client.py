from yaks import YAKS
from yaks import Selector
from yaks import Path
from yaks import Value
import sys
import json


def obs(kvs):
    print('Called OBSERVER KVS: {}'.format(kvs))


def evcb(path, param):
    print('Executing eval on {}'.format(path))
    return Value('executed {}'.format(param))


def main():
    print('creating api')
    y = YAKS()
    y.login(sys.argv[1])
    print('>> Create storage')
    input()
    myst_id = 100
    storage_selector = Selector('/myyaks')
    properties = {'is.yaks.storage.selector': storage_selector}
    y.create_storage(myst_id, properties)
    print('>> Create access and subscription')
    input()
    workspace = y.workspace(Path('/myyaks'))

    sid = workspace.subscribe(Selector('/myyaks/example/**'), obs)

    print('>> Put Tuple')
    input()
    workspace.put(Path('/myyaks/example/one'), Value('hello!'))

    print('>> Put Tuple')
    input()
    workspace.put(Path('/myyaks/example/two'), Value('hello2!'))

    print('>> Put Tuple')
    input()
    workspace.put(Path('/myyaks/example/three'), Value('hello3!'))

    print('>> Put Tuple JSON as RAW')
    input()
    d = Value(json.dumps({'this': 'is', 'a': 'json'}))
    workspace.put(Path('/myyaks/example/four'), d)

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get(Selector('/myyaks/example/one'))))

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get(Selector('/myyaks/example'))))

    print('>> Get Tuple')
    input()
    print('GET: {}'.format(workspace.get(Selector('/myyaks/example/*'))))

    print('>> Put Eval')
    input()
    workspace.eval(Path('/myyaks/key1'), evcb)

    print('>> Get on Eval')
    input()
    print('GET: {}'.format(workspace.get(Selector('/myyaks/key1?[param=1]'))))

    print('>> Dispose Access')
    input()
    if sid:
        workspace.unsubscribe(sid)
    workspace.dispose()

    print('>> Dispose Storage')
    input()
    y.remove_storage(myst_id)
    y.logout()
    print('bye!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} <yaks server address>'.format(sys.argv[0]))
        exit(-1)
    main()
