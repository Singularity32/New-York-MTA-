import csv
import datetime
from pylab import *
from matplotlib.pylab import plt
from matplotlib import dates as mtd
from matplotlib.dates import HourLocator, DayLocator,DateFormatter
f1=open("./Turnstile/Turnstile-Data.txt","rb")
#f2=open("./Turnstile/Sp170St.txt","wb")
rv=csv.reader(f1)
#ro=csv.writer(f2)
fig=plt.figure(figsize=(10,8))
ax1=fig.add_subplot(3,1,1)
ax2=fig.add_subplot(3,1,3)
print "The station we are analyzing is 170th Street on line 4"
REMOTE="R243"; BOOTH="R284" # This is the code for the subway stop
print "We are considering turnstile numbers over the weekday from Jan 7th to Jan 11, 2013"
T_ent=-1     # Entry count on turnstile
T_exit=-1   # Exit count on turnstile
trun=[]
SCP=""
flag=-1
for rw in rv:
 if (rw[0]==BOOTH and rw[1]==REMOTE) :
   flag=1
   print len(rw)
   if SCP!=rw[2]:
     T_ent=-1     # Entry count on turnstile
     T_exit=-1   # Exit count on turnstile
     SCP=rw[2]
   RC_LEN=5                # Length of each turnstile record at a given time (this excludes first three elements in each row)
   j=3
   while j<len(rw):
    wd=rw[j].split('-'); 
    if int(wd[1]) <=11 and int(wd[1])>=7 and rw[j+2]=="REGULAR" : 
     dt=datetime.date(int("20"+wd[2]),int(wd[0]),int(wd[1]))
     tm=rw[j+1].split(":")
     dtm=datetime.time(int(tm[0]),int(tm[1]),int(tm[2]))
     T_tm=datetime.datetime.combine(dt,dtm)     # Converting time to the datetime format in python
     if (T_ent <0):
      T_ent=int(rw[j+3])      # Update entry count on turnstile
      T_exit=int(rw[j+4])    # Update exit count on turnstile
      trun.append([SCP,T_tm, 0,0])      
     else :
      trun.append([SCP,T_tm,int(rw[j+3])-T_ent ,int(rw[j+4])-T_exit])      
      T_ent=int(rw[j+3]) 
      T_exit=int(rw[j+4]) 
    j=j+5   
 elif flag >0 :
  break;
sum_EE =[]
ct=0
j=0
T_ent_t=0; T_exit_t=0   # Total entry and exit for a given time from all the turnstiles respectively.
SCP= trun[0][0]
for line in trun :
 if ct==0 and line[0]==SCP:
  sum_EE.append([line[1], line[2],line[3]])
 else:
  ct=1 
  if line[0]!=SCP :
   j=0
   SCP=line[0]
  sum_EE[j][1]=sum_EE[j][1]+ line[2]
  sum_EE[j][2]=sum_EE[j][2]+ line[3]
  j=j+1

sum_T =transpose(sum_EE) 
tmx =sum_T[0][:]  
y1 =sum_T[1][:]
y2 =sum_T[2][:]
# print jt[0].isoformat(' '),jt[1],jt[2] 
ax1.plot(tmx,y1, label="Entry")
ax1.plot(tmx,y2,label="Exit")
ax1.set_xticklabels(["M","Tu","W", "Th","F"])
wkd=[]
for j in range(7,12):
 dt=datetime.time(12,00,00)
 dd=datetime.date(2013,01,j)
 wkd.append(datetime.datetime.combine(dd,dt))
ax1.set_xticks(wkd)
ax1.set_ylim(0,6000)
ax1.set_xlabel("Day of Week")
fig.suptitle("Entry and Exit at 170th Street, Bronx (Line 4)")
ax1.set_title("Number of people entering and exiting subway stop every 3 hours (Weekdays)")
ax1.legend(loc=0,prop={'size':8})
wed=[]
for j in sum_EE :
 if j[0].isoweekday()==3: wed.append(j)
twed=transpose(wed)
ax2.plot(twed[0][:],twed[1][:],label="Entry")
ax2.plot(twed[0][:],twed[2][:],label="Exit")
ax2.xaxis.set_major_formatter(DateFormatter("%H:%M"))
ax2.xaxis.set_major_locator(HourLocator(interval=3))
ax2.set_title("Number of people entering and exiting subway stop every 3 hours (Wednesday)")
legend()
savefig("./Turnstile/170St-4.png")
plt.show()
