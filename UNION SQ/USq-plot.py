import csv
import array
import datetime
from datetime import time
from matplotlib import pyplot as plt 
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
from matplotlib.dates import DateFormatter, HourLocator
fig=plt.figure(1)
ax=fig.add_subplot(111)
f1=open("USq-TimeInt.txt","rb")
nr=csv.reader(f1)
first=nr.next()
ct=0
arrx=[]
arry=[]
arx=[]
ary=[]
for num  in range(3):
 ct=0;
 print num
 del arrx[:],arry[:]
 for line in nr:
  if (len(line[0])==3):
   break
  tm=line[0].split(':')
  if int(tm[0])>=24 : 
    ct=ct+1
    if ct==1:
     dt=datetime.datetime.strptime('23:59:59','%H:%M:%S')
     arrx.append(dt)
     arry.append(arry[-1])
  tm =str(int(tm[0])%24)+':'+str(int(tm[1]))+':'+str(int(tm[2]))
  #tme=time(int(tm[0])%24,int(tm[1]),int(tm[2]))
  dt=datetime.datetime.strptime(tm,'%H:%M:%S')
  arrx.append(dt)
  arry.append(line[1])
#hfm=dates.DateFormatter('%H:%m:%S')
#plt.axis.xaxis.set_major_formatter(hfm)
 lm=len(arrx)
 for j in range(lm-ct, lm):
  arx.append(arrx[j])
  ary.append(arry[j])
 for j in range(0,lm-ct) :
  arx.append(arrx[j])
  ary.append(arry[j]) 
 print ary
 if (num==0):
  ax.plot(arx,ary,drawstyle='steps-post',label='4 WKD')
 elif num==1:  
  ax.plot(arx,ary,linestyle='--',drawstyle='steps-post',label='4 SAT')
 elif num==2:  
  ax.plot(arx,ary,linestyle='-',drawstyle='steps-post',label='4 SUN')
 del arx[:],ary[:]
plt.ylim([0,25])
ax.legend(loc='best')
plt.gca().xaxis.set_major_locator(HourLocator(interval=3) )
plt.gca().xaxis.set_major_formatter( DateFormatter('%H:%M:%S') )
plt.show() 
