from yaks import Yaks
from yaks import Value
from yaks import Encoding

y = Yaks.login(None)
ws = y.workspace('/demo/')

while True:
    f = input(
        ':> input a filter expression in x,\
            such as \"x > 40\", \"x%2 == 0\":\n:>')
    ws.put('/demo/fprod/filter', Value(f, encoding=Encoding.STRING))
