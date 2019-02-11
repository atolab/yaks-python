from yaks import Yaks 
import jsonpickle
import random
import sys 
import time

filter = "x > 50"

def update_filter(kvs):
    global filter
    for kv in kvs:        
        _,v = kv                
        filter = v.value
        print('New Filter: {}'.format(v))        


def main(addr):
    y = Yaks.login(addr)
    ws = y.workspace('/demo/fprod')
    ws.subscribe('/demo/fprod/filter', update_filter)

    while(True):
        x = random.randint(0, 100) 
        ## The filter is evaluated in the current context
        if eval (filter) == True:
            print (x)
        else:
            print ('Filtered...')
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('[Usage] {} <yaks server address>'.format(sys.argv[0]))
        exit(-1)
    
    addr = sys.argv[1]
    main(addr)