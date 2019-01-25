from yaks import Yaks
from yaks import Value
from yaks import Selector
from yaks import Path
from yaks import Encoding
from papero import Property
import sys

# CREATE TABLE test (id SERIAL NOT NULL PRIMARY KEY,
#  mystring VARCHAR(255), myint INT, myfloat REAL, mydate DATE);
# INSERT INTO test VALUES (1, 'test1', 1, 1.1, '2018-01-01');
# INSERT INTO test VALUES (2, 'test2', 2, 2.2, '2018-02-02');
# INSERT INTO test VALUES (3, 'test3', 3, 3.3, '2018-03-03');


def main():
    print('creating api')
    y = Yaks.login(sys.argv[1])
    admin = y.admin()

    print('>> Create memory storage')
    input()
    storage1 = 's1'
    admin.add_storage(storage1, [
        Property('selector', '/is/test/mem/**'),
        Property('is.yaks.backend.kind', 'memory')])

    # print('>> Create SQL storage on legacy table "test"')
    # input()
    # storage2 = 's2'
    # admin.add_storage(storage2, [
    #     Property('selector', '/is/test/db/leg-table'),
    #     Property('is.yaks.backend.kind', 'dbms'),
    #     Property('is.yaks.backend.sql.table', 'test')])

    print('>> Create SQL storage on a new key/value '
          'table which will be droped at storage disposal')
    input()
    storage3 = 's3'
    admin.add_storage(storage3, [
        Property('selector', '/is/test/db/new-table/**'),
        Property('is.yaks.backend.kind', 'dbms'),
        Property('is.yaks.backend.sql.on_dispose', 'drop')])

    print('>> Create workspace')
    input()
    workspace = y.workspace(Path('/is/test/db'))

    print('****** SQL storage - key/value table ********')

    print('>> Put /is/test/db/new-table/A/B')
    input()
    workspace.put(Path('new-table/A/B'),
                  Value("BCD", encoding=Encoding.STRING))

    print('>> Put /is/test/db/new-table/A/D')
    input()
    workspace.put(Path('new-table/A/D'),
                  Value("DEF", encoding=Encoding.STRING))

    print('>> Put /is/test/db/new-table/A/B/G')
    input()
    workspace.put(Path('new-table/A/B/G'),
                  Value("GHI", encoding=Encoding.STRING))

    print('>> Put /is/test/db/new-table/A/B/H/I/J')
    input()
    workspace.put(Path('new-table/A/B/H/I/J'),
                  Value("JKL", encoding=Encoding.STRING))

    print('>> Get /is/test/db/new-table/A/B')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/B'))))

    print('>> Get /is/test/db/new-table/A/*')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/*'))))

    print('>> Get /is/test/db/new-table/A/**')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/**'))))

    print('>> Get /is/test/db/new-table/A/**/J')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/**/J'))))

    print('>> Put /is/test/db/new-table/A/B/G')
    input()
    workspace.put(Path('new-table/A/B/G'),
                  Value("XXXX", encoding=Encoding.STRING))

    print('>> Get /is/test/db/new-table/A/**')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/**'))))

    print('>> Get /is/test/db/new-table/A/**?v=\'XXXX\'')
    input()
    print('GET: {}'.format(workspace.get(
        Selector("new-table/A/**?v='XXXX'"))))

    print('>> Remove /is/test/db/new-table/A/D')
    input()
    workspace.remove(
        Path('new-table/A/D'))

    print('>> Get /is/test/db/new-table/A/D')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/D'))))

    print('>> Remove /is/test/db/new-table/A/B')
    input()
    workspace.remove(
        Path('new-table/A/B'))

    print('>> Get /is/test/db/new-table/A/B/**')
    input()
    print('GET: {}'.format(workspace.get(
        Selector('new-table/A/B/**'))))

    # print('****** SQL storage - legacy table ********')

    # print('>> Get /is/test/db/leg-table')
    # input()
    # print('GET: {}'.format(workspace.get(
    #     Selector('leg-table'))))

    # print('>> Put /is/test/db/leg-table')
    # input()
    # workspace.put(
    #     Path('leg-table'),
    #     Value(["4", "test4", "4", "4.4", '2018-04-04'],
    #     encoding=Encoding.SQL))

    # print('>> Get /is/test/db/leg-table')
    # input()
    # print('GET: {}'.format(workspace.get(
    #     Selector('leg-table'))))

    print('****** DISPOSE ALL ********')

    print('>> Dispose Storage1')
    input()
    admin.remove_storage(storage1)

    # print('>> Dispose Storage2')
    # input()
    # admin.remove_storage(storage2)

    print('>> Dispose Storage3')
    input()
    admin.remove_storage(storage3)

    y.logout()
    print('bye!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} <yaks server address>'.format(sys.argv[0]))
        exit(-1)
    main()
