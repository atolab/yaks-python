from yaks import YAKS
from yaks import Value
from yaks import Selector
from yaks import Path
from yaks.encoding import SQL
import sys

# CREATE TABLE test (id SERIAL NOT NULL PRIMARY KEY,
#  mystring VARCHAR(255), myint INT, myfloat REAL, mydate DATE);
# INSERT INTO test VALUES (1, 'test1', 1, 1.1, '2018-01-01');
# INSERT INTO test VALUES (2, 'test2', 2, 2.2, '2018-02-02');
# INSERT INTO test VALUES (3, 'test3', 3, 3.3, '2018-03-03');


def main():
    print('creating api')
    y = YAKS()
    y.login(sys.argv[1])

    print('>> Create memory storage')
    input()
    storage1 = 's1'
    y.create_storage(storage1, properties={
        'is.yaks.storage.selector': Selector('/is/test/mem'),
        'is.yaks.backend.kind': 'memory'})

    print('>> Create SQL storage on legacy table "test"')
    input()
    storage2 = 's2'
    y.create_storage('/is/test/db/leg-table',
                                   {'is.yaks.backend.kind': 'dbms',
                                    'is.yaks.backend.sql.table': 'test'})

    print('>> Create SQL storage on a new key/value '
          'table which will be droped at storage disposal')
    input()
    storage3 = y.create_storage(storage1, properties={
        'is.yaks.storage.selector': Selector('/is/test/db/new-table'),
        'is.yaks.backend.kind': 'dbms',
        'is.yaks.backend.sql.on_dispose': 'drop'})

    print('>> Create workspace')
    input()
    workspace = y.workspace(Path('/is/test/'))

    print('****** SQL storage - key/value table ********')

    print('>> Put /is/test/db/new-table/A/B')
    input()
    workspace.put(Path('/is/test/db/new-table/A/B'), Value("BCD"))

    print('>> Put /is/test/db/new-table/A/D')
    input()
    workspace.put(Path('/is/test/db/new-table/A/D'), Value("DEF"))

    print('>> Put /is/test/db/new-table/A/B/G')
    input()
    workspace.put(Path('/is/test/db/new-table/A/B/G'), Value("GHI"))

    print('>> Put /is/test/db/new-table/A/B/H/I/J')
    input()
    workspace.put(Path('/is/test/db/new-table/A/B/H/I/J'), Value("JKL"))

    print('>> Get /is/test/db/new-table/A/B')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/B'))))

    print('>> Get /is/test/db/new-table/A/*')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/*'))))

    print('>> Get /is/test/db/new-table/A/**')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/**'))))

    print('>> Get /is/test/db/new-table/A/**/J')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/**/J'))))

    print('>> Put /is/test/db/new-table/A/B/G')
    input()
    workspace.put(Path('/is/test/db/new-table/A/B/G'), Value("XXXX"))

    print('>> Get /is/test/db/new-table/A/**')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/**'))))

    print('>> Get /is/test/db/new-table/A/**?v=\'XXXX\'')
    input()
    print('GET: {}'.format(workspace.get(
        Selector("/is/test/db/new-table/A/**?v='åXXXX'"))))

    print('>> Remove /is/test/db/new-table/A/D')
    input()
    workspace.remove(
        Path('/is/test/db/new-table/A/D'))

    print('>> Get /is/test/db/new-table/A/D')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/D'))))

    print('>> Remove /is/test/db/new-table/A/B')
    input()
    workspace.remove(
        Path('/is/test/db/new-table/A/B'))

    print('>> Get /is/test/db/new-table/A/B/**')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/new-table/A/B/**'))))

    print('****** SQL storage - legacy table ********')

    print('>> Get /is/test/db/leg-table')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/leg-table'))))

    print('>> Put /is/test/db/leg-table')
    input()
    workspace.put(
        Path('/is/test/db/leg-table'),
        Value(["4", "test4", "4", "4.4", '2018-04-04'], encoding=SQL))

    print('>> Get /is/test/db/leg-table')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('/is/test/db/leg-table'))))

    print('****** DISPOSE ALL ********')

    print('>> Dispose Access')
    input()
    workspace.dispose()

    print('>> Dispose Storage1')
    input()
    y.remove_storage(storage1)

    print('>> Dispose Storage2')
    input()
    y.remove_storage(storage2)

    print('>> Dispose Storage3')
    input()
    y.remove_storage(storage3)

    y.logout()
    print('bye!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} <yaks server address>'.format(sys.argv[0]))
        exit(-1)
    main()
