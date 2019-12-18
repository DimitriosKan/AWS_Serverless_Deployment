import time
import sys
import os

print ('Waiting ...\n')
x = True
while x:
    sys.stdout.write('[')
    sys.stdout.flush()
    for i in range(10,0,-1):
        sys.stdout.write(f'$')
        sys.stdout.flush()
        time.sleep(1)
    x = False
    print (']')
print ('\n Complete !')

#sleep = time.sleep(1)
#print (sleep)
#while sleep != 0:
#    print ('Waiting ...')
