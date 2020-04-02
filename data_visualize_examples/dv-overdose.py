import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.animation as animation    

from .. import trace
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

def augment(xold,yold,numsteps):
    xnew = []
    ynew = []
    for i in range(len(xold)-1):
        difX = xold[i+1]-xold[i]
        stepsX = difX/numsteps
        difY = yold[i+1]-yold[i]
        stepsY = difY/numsteps
        for s in range(numsteps):
            xnew = np.append(xnew,xold[i]+s*stepsX)
            ynew = np.append(ynew,yold[i]+s*stepsY)
    return xnew,ynew
    
def smoothListGaussian(listin,strippedXs=False,degree=10):  
    window=degree*2-1  
    weight=np.array([1.0]*window)  
    weightGauss=[]  
    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(np.exp((4*(frac))**2))  
        weightGauss.append(gauss)
    weight=np.array(weightGauss)*weight  
    smoothed=[0.0]*(len(listin)-window)  
    for i in range(len(smoothed)):
        smoothed[i]=sum(np.array(listin[i:i+window])*weight)/sum(weight)  
    return smoothed


overdoses = pd.read_excel('\\datas\\overdose_data_1999-2015.xls',sheet_name='Online',skiprows =6)
def get_data(table,rownum,title):
    data = pd.DataFrame(table.loc[rownum][2:]).astype(float)
    data.columns = {title}
    print(data)
    return data


title = 'Heroin Overdoses'
d = get_data(overdoses,18,title)
x = np.array(d.index)
y = np.array(d['Heroin Overdoses'])
# overdose = pd.DataFrame(y,x)
XN,YN = augment(x,y,10)
overdose = pd.DataFrame(smoothListGaussian(YN),smoothListGaussian(XN))
print( 'len of XN:', len(XN), '\nlen of YN:', len(YN), '\nshape of overdose:', overdose.shape)
# overdose = augmented
overdose.columns = {title}

Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=180)


fig = plt.figure(figsize=(10,6), dpi=72, tight_layout=True)

plt.xlim(1999, 2016)
plt.ylim(np.min(overdose)[0], np.max(overdose)[0])
plt.xlabel('Year',fontsize=15)
plt.ylabel(title,fontsize=15)
plt.title('Heroin Overdoses per Year',fontsize=18)
print("complete fig")



def animate(i):
    print(i, type(i), end="\n")
    #data = overdose.iloc[:int(i+1)] #select data range
    data = overdose.iloc[:int(i+1)]
    p = sns.lineplot(x=data.index, y=data[title], data=data, color='b')
    p.tick_params(labelsize=12)
    plt.setp(p.lines, linewidth=2)
    return p,

try:

    # ani = matplotlib.animation.FuncAnimation(fig, animate, frames=160, interval=10, blit=True,  repeat=True)
    print(len(overdose))
    ani = matplotlib.animation.FuncAnimation(fig, animate, blit=True, interval=50)
    plt.show()
except Exception as e:
    getException(e)



