#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
filename = 'time_line.log'

INTERVAL_SIZE =20

interval_list = []

k  = 0
t  =0

data = np.loadtxt(filename)                                                              
print(data.shape)

x1, y1 =[], []
#for i in range(900000, 900500):
for i in range(10000, len(data)):
    t += data[i]
    x1.append(t)
    if k != INTERVAL_SIZE-1:
        k += 1
        y1.append(data[i]) 
        interval_list.append(data[i])
    else:
        interval_list.append(data[i])
        y1.append(sum(interval_list)/INTERVAL_SIZE)
        interval_list.remove(interval_list[0])
    
     

#print(x1)
#print(y1)
fig = plt.figure(1)
ax = fig.add_subplot(111)
#ax.plot(x1[8000:-60000],y1[8000:-60000])
ax.plot(x1,y1,linewidth=0.15)
plt.show()

