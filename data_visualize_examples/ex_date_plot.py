import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange, date2num)
import numpy as np
from datetime import datetime, timedelta
import time

# Fixing random state for reproducibility
np.random.seed(19680801)


# tick every 5th easter
rule = rrulewrapper(YEARLY, byweekday=2, interval=1)
loc = RRuleLocator(rule)

formatter = DateFormatter('%Y/%m/%d')
date1 = datetime(2020, 1, 1)
date2 = datetime(2020, 4, 3)
delta = timedelta(days=1)

dates = drange(date1, date2, delta)
testdate1 = datetime.strptime('20191209', '%Y%m%d')
testdate2 = datetime.strptime('20200101', '%Y%m%d')
print('type of testdate:',type(testdate1))
print('type:',type(dates[0]))
x = [date2num(testdate1),date2num(testdate2)]
s = np.random.rand(len(x))  # make up some random y values


fig, ax = plt.subplots()
plt.plot_date(x, s)
ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_tick_params(rotation=30, labelsize=10)

plt.show()