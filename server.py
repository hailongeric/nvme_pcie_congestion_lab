#!/usr/bin/python3
from socket import *
from socket_utils import *
import numpy

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 25000))
s.listen(1)
c,a = s.accept()


for _ in range(10000):  
    a = numpy.arange(0, 1024*1024) # 1M
    send_from(a, c)

    # construct a gap;
    num=0
    for i in range(3000000):
        num+=i
    print(num)


s.close()