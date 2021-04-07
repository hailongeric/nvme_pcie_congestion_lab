#!/usr/bin/python3

import json
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
from matplotlib.pyplot import MultipleLocator


def write_json(file_name, d): 
    with open(file_name,'w') as file_object:
        json.dump(d,file_object)

def read_json(file_name):
    with open(file_name,'r') as file_object:
        c = json.load(file_object)
    return c

f = open("graph1_data.txt")
lines = f.read().split('\n')[6:]
f.close()

graph1_dic_key = []
graph1_dic_value = []
graph1_bd_value = []

dic = {}
for line in lines:
    if not line:
        continue
    
    size, cycles = line.split()
    dic[int(size)] = int(cycles)
    graph1_dic_key.append(int(size))
    graph1_dic_value.append(int(cycles))
    graph1_bd_value.append(1/(int(cycles)*(1/2300000000))/1024)

write_json("data_cycles.json",dic)


fig = plt.figure(figsize=(15, 8))
ax1 = fig.add_subplot(3, 1, 1)
ax1.plot(graph1_dic_key, graph1_dic_value, linewidth=1.5)
ax1.set_ylabel('Cycles(rdtscp)')
ax1.set_xlim(0, 260)

ax2 = fig.add_subplot(3, 1, 2)
ax2.set_ylabel('Bandwidth(KBit/s)')
ax2.plot(graph1_dic_key, graph1_bd_value, linewidth=1.5)
ax2.set_xlim(0, 260)

ax3 = fig.add_subplot(3, 1, 3)
ax3.set_ylabel('ErrorRate(%)')
# ax3.plot([8, 14, 28, 56, 84, 112], [20.55874087613104,  0.4652431450171213,  0.4379143298974435,  0.360177949125539, 0.32246437444485923, 0.2912675740771859], linewidth=1.5)
X = [4,    8,    16,    20,   24 ,  28,   32,   64,   128,  256]
Y = [49.8, 19.5, 0.74,  1.06, 0.78, 2.45, 0.69, 0.55, 1.60, 2.415]
ax3.plot(X, Y, linewidth=1.5)
ax3.set_xlim(0, 260)

plt.xlabel('Data Size(KB)')
plt.show()

'''
分别测试4K, 8K, 16K,20K, 24K ,28K,32K, 64K, 128K, 256K;
4K:  49.77666666666667%
8K:  19.45 %
16K: 0.74 %
20K: 1.0566666666666666 %
24K: 0.7766666666666666 %
28K: 2.4483333333333333 %
32K: 0.69 %
64K: 0.5533333333333333 %
128K: 1.6049999999999998 %
256K: 2.415 %
'''

'''
records length: 240000000
ave_gap 59
739.0
first peak 739.0
Error Rate:  49.579499999999996 %
==============
records length: 240000000
ave_gap 13
34.0
first peak 34.0
Error Rate:  19.933999999999997 %
==============
records length: 240000000
ave_gap 15
28.0
first peak 28.0
Error Rate:  0.6935 %
==============
records length: 240000000
ave_gap 16
14.0
first peak 14.0
Error Rate:  0.9900000000000001 %
==============
records length: 240000000
ave_gap 18
22.0
first peak 22.0
Error Rate:  1.176 %
==============
records length: 240000000
ave_gap 15
25.0
first peak 25.0
Error Rate:  2.2835 %
==============
records length: 240000000
ave_gap 15
20.5
first peak 20.5
Error Rate:  0.6134999999999999 %
==============
records length: 240000000
ave_gap 18
37.0
first peak 37.0
Error Rate:  0.5369999999999999 %
==============
records length: 240000000
ave_gap 28
51.5
first peak 51.5
Error Rate:  1.2385 %
==============
records length: 240000000
ave_gap 53
100.0
first peak 100.0
Error Rate:  1.67 %
==============
'''