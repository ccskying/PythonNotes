# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:52:02 2020

@author: lcc
"""
import matplotlib.pyplot as plt
import numpy as np

step = 10

colors = ['r','b','g']
color_index = [3 for i in range(10)]

cr=np.array([6.2,3.2])
cb=np.array([6.5,3.0])
cg=np.array([6.6,3.7])
points = np.zeros((10,2))
points[0] = [4.6,2.9]
points[1] = [4.7,3.2]
points[2] = [4.9,3.1]
points[3] = [5.0,3.0]
points[4] = [5.1,3.8]
points[5] = [5.5,4.2]
points[6] = [5.9,3.2]
points[7] = [6.0,3.0]
points[8] = [6.2,2.8]
points[9] = [6.7,3.1]

ncount = 0
for i in range(step):
    for j in range(10):
        distance = np.zeros(3)
        diff0 = points[j]- cr
        for k in range(len(diff0)):
            distance[0] += diff0[k]**2
        diff1 = points[j]- cb
        for k in range(len(diff1)):
            distance[1] += diff1[k]**2
        diff2 = points[j]- cg
        for k in range(len(diff2)):
            distance[2] += diff2[k]**2
        #print(distance)
        color_index[j] = np.argmin(distance)
    
    crt = cr
    cbt = cb
    cgt = cg
    cr_count = 0
    cb_count = 0
    cg_count = 0
    cr=np.array([0,0])
    cb=np.array([0,0])
    cg=np.array([0,0])
    for j in range(10):
        if color_index[j] == 0:
            cr = points[j]+cr
            cr_count += 1
        if color_index[j] == 1:
            cb = points[j]+cb
            cb_count += 1
        if color_index[j] == 2:
            cg = points[j]+cg
            cg_count += 1
    cr = cr / cr_count
    cb = cb / cb_count
    cg = cg / cg_count

    ncount += 1
    print('loop time:',ncount,'red center',cr,'blue center',cb,'green center',cg)
    if (crt == cr).all() and (cbt == cb).all() and (cgt == cg).all():
        break
            
print('converge done at No.',ncount,'iteration')
for i in range(10):
    plt.scatter(points[i][0],points[i][1], color=colors[color_index[i]],marker='^')
    
plt.scatter(cr[0],cr[1],color='r')
plt.scatter(cb[0],cb[1],color='b')
plt.scatter(cg[0],cg[1],color='g')