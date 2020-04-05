import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation
import random 
from time import sleep
from datetime import datetime, timedelta
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange, date2num)
import pandas as pd


country = ['Taiwan',
           'China',
           'France',
           'Italy',
           'Japan',
           'Philippines',
           'South Korea',
           'Spain',
           'United Kingdom',
           'United States',
           'World'] #can read data from country standard

colors = ['#1f77b4',
          '#ff7f0e',
          '#2ca02c',
          '#d62728',
          '#9467bd',
          '#8c564b',
          '#e377c2',
          '#7f7f7f',
          '#bcbd22',
          '#17becf',
          '#1a55FF'] #can random generate

# mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)


xdata, ydata = [], []
lines = []

def load_data(filepath="covid-19-get-data\\public\\data\\ecdc\\full_data.csv"):
    """取得csv檔裡面的數據，轉換成dataframe，使用location當作index，過濾country的部分

    Parameters:
    filepath (str): 資料路徑

    Returns:
    df (pandas.dataframe):  指定地點的全部數據

   """

    df = pd.read_csv(
        filepath,
        keep_default_na=False,
        encoding="UTF-8",
        engine='python'
    )
    for i in range(df['date'].shape[0]):
        #print(df.at[i,'date'])
        df.at[i,'date']=date2num(datetime.strptime(df['date'][i],'%Y-%m-%d'))


    df = df.set_index('location')
    df = df.loc[country]
    print(df.describe)
    return df 

def data_filter(df, data_field='new_cases'):
    """取得要的欄位，轉成List
    Parameters:
    df (dataframe): country index 過濾地點後的資料
    data_filed (str):

    Returns:
    df (list):  特定欄位的數據

    """
    case_data = []

    df = df.filter(items=['date',data_field])
        

    for i , element in enumerate(country):
        temp_df = df.loc[element]
        case_data.extend([[temp_df['date'].tolist(),temp_df[data_field].tolist()]])

    return case_data



def main():

    #產生畫布
    fig = plt.figure(figsize=(15,6),dpi=150)
    ax = plt.axes([0.1, 0.1, 0.6, 0.75], ylim = (1,10000))
    plt.yscale("log")

    #設定線條
    for index in range(len(country)):
        lobj = ax.plot([], [], lw=2, color=colors[index])[0]
        lines.append(lobj)

    #設定樣式
    plt.style.use('fivethirtyeight')
    
    #設定X軸格式
    rule = rrulewrapper(YEARLY, byweekday=2, interval=1)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%Y/%m/%d')

    #設定軸
    ax.grid()
    
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)

    #設定標籤
    plt.xlabel('date')
    plt.ylabel('cases')
    
            

    #取得資料
    df = load_data()

    #轉換資料形式
    case_data = data_filter(df)

    date1 = datetime(2020, 1, 1)
    date2 = datetime(2020, 4, 3)
    delta = timedelta(days=1)

    dates = drange(date1, date2, delta)
    print(dates)

    def init():
        for line in lines:
            line.set_data([],[])
        for i in range(len(country)):
            ax.plot([],label=str(country[i]))
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        return lines



    def animate(i):
        xdata = []
        ydata = []
        print('animate')
        # update the data
        print(i)
        for t in range(len(country)): #iterate every country
            x = case_data[t][0][0:i+1]
            y = case_data[t][1][0:i+1]
            
            print("type of x:",type(x))

            #xdata.append(date2num([datetime.strptime(x[0],'%Y-%m-%d')])[0])
            #xdata.append(dates[i])
            #xdata.append([date2num([datetime.strptime(x[0],'%Y-%m-%d')])[0].tolist()])
            xdata.append(x)
            ydata.append(y)
            
        print(xdata, ydata)
        for lnum,line in enumerate(lines):
            #print(xdata[lnum],ydata[lnum])
            #line.set_data(xdata[lnum], ydata[lnum])
            
            plt.plot_date(xdata[lnum],ydata[lnum],'-', lw=1)
        
        return lines

    ani = animation.FuncAnimation(fig, animate, init_func=init, blit=False, interval=10, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()