#!/usr/bin/python3
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat

print(sys.argv[1])
filename = sys.argv[1]


INTERVAL_SIZE =50

interval_list = []

k  = 0
t  =0

data = np.loadtxt(filename)                                                              
print(data.shape)

x1, y1 =[], []
#for i in range(900000, 900500):
for i in range(10000, len(data)):
    t += data[i]
    # x1.append(t)
    # y1.append(data[i]) 
    # if data[i] > 1.27341e-6 or data[i] < 1.15199e-6:
    #     continue
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

mat_x = np.array(x1[100000:750000])
mat_y = np.array(y1[100000:750000])

mat_x = [mat_x[i] for i in range(0,len(mat_x),20)]
mat_y = [mat_y[i] for i in range(0,len(mat_y),20)]

mdic = {"time":mat_x, "response_time":mat_y}


savemat("{}.mat".format(filename.split('.')[0]), mdic)


ax.plot(mat_x,mat_y,linewidth=0.15)
plt.show()

