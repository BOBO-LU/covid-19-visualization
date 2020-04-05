
"""
https://stackoverflow.com/questions/23049762/matplotlib-multiple-animate-multiple-lines
"""
import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import random 
import numpy as np
import time

fig = plt.figure()
ax1 = plt.axes(xlim=(-108, -104), ylim=(31,34))

plt.xlabel('Longitude')
plt.ylabel('Latitude')

plotlays, plotcols = [2], ["black","red", "blue"]
lines = []
for index in range(3):
    lobj = ax1.plot([],[],lw=2,color=plotcols[index])[0]
    lines.append(lobj)

print(lines)
def init():
    for line in lines:
        line.set_data([],[])
    return lines

x1,y1 = [],[]
x2,y2 = [],[]
x3,y3 = [],[]

# fake data
frame_num = 100
gps_data = [-104 - (4 * random.rand(2, frame_num)), 31 + (3 * random.rand(2, frame_num))]

print(gps_data)
print("type of gps_data",type(gps_data))
print(np.array(gps_data).shape)
print(len(gps_data[0]))
print(len(gps_data[1]))
def animate(i):
    #print(i)
    x = gps_data[0][0, i]
    y = gps_data[1][0, i]
    x1.append(x)
    y1.append(y)
    #print('gps_data:',x)
    x = gps_data[0][1,i]
    y = gps_data[1][1,i]
    x2.append(x)
    y2.append(y)

    x = gps_data[0][1,i]+.1
    y = gps_data[1][1,i]+.1
    x3.append(x)
    y3.append(y)

    xlist = [x1, x2, x3]
    print('xlist:',xlist)
    ylist = [y1, y2, y3]
    print('ylist:',ylist)

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        #print('set_data: ',xlist[lnum],ylist[lnum])

        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 
    print(xlist,ylist)
    #print('lines:',lines)
    time.sleep(3)
    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frame_num, interval=10, blit=True)


plt.show()