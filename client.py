#!/usr/bin/python3
import numpy
from socket import *
from socket_utils import *


c = socket(AF_INET, SOCK_STREAM)
c.connect(('10.177.74.126', 25000))


#a = numpy.zeros(shape=1000000000, dtype=int)
#a[0:10]
for _ in range(1000000):
    a = numpy.zeros(shape=1024*1024, dtype=int) #1K
    recv_into(a, c)

c.close()