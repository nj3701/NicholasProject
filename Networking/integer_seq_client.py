import socket
import sys
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect( (sys.argv[1], int(sys.argv[2])) )
    f = s.makefile('rw')

    for i in range(1, int(sys.argv[3])):
        f.write(str(i) + "\n")
        f.flush()


    f.write("-1\n")
    f.flush()
    l= f.readline()
    print(l)
    f.close()
