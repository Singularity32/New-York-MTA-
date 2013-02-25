import csv
import datetime
from pylab import *
from matplotlib.pylab import plt
from matplotlib import dates as mtd
from matplotlib.dates import HourLocator, DayLocator,DateFormatter
def diffelem(tn):
    for j,ln in enumerate(tn):
       if j%42 == 0: s_ent,s_ext=0,0
       if j%42 !=41:  
           ln[2]=tn[j+1][2]-ln[2]
           ln[3]=tn[j+1][3]-ln[3]
           print j,ln[0],ln[1].day
           if j%6==5:
              s_ent=s_ent+ln[2]
              s_ext=s_ext+ln[3]
       else:
           ln[2]=int(s_ent/6)
           ln[3]=int(s_ext/6)   
           #print ln[2],ln[3]
f1=open("./Turnstile/Turnstile-Data.txt","rb")
f2=open("./Turnstile/RBS.csv","rb")
f3=open("./Subway Info/StationEntrances.csv","rb")
#f2=open("./Turnstile/Sp170St.txt","wb")
rv=csv.reader(f1)
rv2=csv.reader(f2)
rv3=csv.reader(f3)
#ro=csv.writer(f2)
print "Enter the name of the MTA Subway stop.  For stops that have only street number, enter the street number in arabic numerals. You may also enter only one word for the stop. For example, if Union Square is the stop,  you may enter Union or Square "
fl=0;
RB=[]
while fl==0 :
 stp= raw_input('-->')
 f2.seek(0)
 for rc in rv2:
  if len(rc) ==1 :break;
  if rc[2].lower().find(stp.lower()) >-1 and fl==0:
   print "Do you mean the stop: ", rc[2],  "with lines ", rc[3]
   etr=raw_input("Y/N  ")
   if etr.lower()=='y': 
     RB.append([rc[0],rc[1]])         #This stoes the REMOTE and BOOTH data of the stop. 
     print RB[-1]
     rn=rc[2]
     lns=rc[3]
     fl=1                             # Flag variale indicating that the station name has been found.
  elif fl==1:   
   if rc[2]==rn and rc[3]==lns:
     RB.append([rc[0],rc[1]])          # If there is more than one occurence of the input station in the records (each record has a unique (REMOTE, BOOTH) pair/
     print RB[-1]
 if fl==0:
  print "There is no stop by that name. Please enter a different station number"
rn=rn.replace('/','-')
print "The station we are analyzing is; ", rn
print "We are considering turnstile numbers over the weekday from Jan 7th to Jan 11, 2013"
T_ent=-1     # Entry count on turnstile
T_exit=-1   # Exit count on turnstile
trun=[]
SCP=""
irr=[]
flag=-1
for fpos,rw in enumerate(rv):
 for et in RB:             
	 if (rw[0]==et[1] and rw[1]==et[0]) :  # Determining if the station remote and booth data of the input station matches the turnstile record.    
	   #print fpos
	   if SCP!=rw[2]:
             if  flag>0 and T_ledge.hour==23 and T_ledge.isoweekday()==5:
	         trun.append([SCP,T_ledge,C_ent_p, C_ext_p])
	     C_ent_p=int(rw[6])    # Entry count on turnstile
	     C_ext_p=int(rw[7])   # Exit count on turnstile
	     SCP=rw[2]
	     wd=rw[3].split('-'); 
	     dt=datetime.date(int("20"+wd[2]),int(wd[0]),int(wd[1]))
	     tm=rw[4].split(":")
	     dtm=datetime.time(int(tm[0]),int(tm[1]),int(tm[2]))
             dtm_ledge=datetime.time(3,0,0)
             T_ledge = datetime.datetime.combine(dt,dtm_ledge)
	     T_tm_prev=datetime.datetime.combine(dt,dtm)     # Converting time to the datetime format in python
             while T_ledge<=T_tm_prev :
	         trun.append([SCP,T_ledge,C_ent_p, C_ext_p])
                 T_ledge+=datetime.timedelta(0,4*60*60)
           RC_LEN=5                # Length of each turnstile record at a given time (this excludes first three elements in each row)
	   j=3
	   while j<len(rw):
             flag=1
	     wd=rw[j].split('-')
	     dt=datetime.date(int("20"+wd[2]),int(wd[0]),int(wd[1]))
	     tm=rw[j+1].split(":")
	     dtm=datetime.time(int(tm[0]),int(tm[1]),int(tm[2]))
	     T_tm=datetime.datetime.combine(dt,dtm)     # Converting time to the datetime format in python
	     #T_delta=  (T_tm.day- T_tm_prev.day)*24 + T_tm.hour - T_tm_prev.hour
             T_delta=T_tm-T_tm_prev
	     C_ent=int(rw[j+3])      # Update entry count on turnstile
	     C_ext=int(rw[j+4])    # Update exit count on turnstile
           #  if (T_ledge<=T_tm_prev):
	    #     trun.append([SCP,T_ledge,C_ent, C_ext])
             #    T_ledge+=datetime.timedelta(0,4*60*60)
             while T_ledge<=T_tm :
                 r_cnt_ent= C_ent_p + float((T_ledge - T_tm_prev).seconds)/T_delta.seconds * (C_ent -C_ent_p)
                 r_cnt_ext= C_ext_p + float((T_ledge - T_tm_prev).seconds)/T_delta.seconds * (C_ext -C_ext_p)
	         trun.append([SCP,T_ledge,r_cnt_ent, r_cnt_ext])
                 T_ledge+=datetime.timedelta(0,4*60*60)
             C_ent_p=C_ent
             C_ext_p=C_ext
             if rw[j+2]!="REGULAR" : irr.append([SCP,T_tm]) 
	     T_tm_prev=T_tm 
             #if T_ledge.hour==23 : print T_ledge.isoweekday(),j,len(rw)
	     j=j+RC_LEN   
if  T_ledge.hour==23 and T_ledge.isoweekday()==5:
 trun.append([SCP,T_ledge,C_ent_p, C_ext_p])
diffelem(trun)
sum_EE =[]
ct=0
j=0
T_ent_t=0; T_exit_t=0   # Total entry and exit for a given time from all the turnstiles respectively.
SCP= trun[0][0]

for line in trun :
 if ct==0 and line[0]==SCP:
	  sum_EE.append([line[1], line[2],line[3]])
	  j=j+1
 else:
	  ct=1 
	  if line[0]!=SCP :
		   j=0
		   SCP=line[0]

	  ln =sum_EE[j]
	  if (ln[0].day==line[1].day and ln[0].hour==line[1].hour):
	      ln[1]=ln[1]+ line[2]
	      ln[2]=ln[2]+ line[3]
	  else:
	      print "Array trun is not properly aligned"   
	  j=j+1


sum_T =transpose(sum_EE) 
tmx_wkd,tmx_wnd=[],[]
y1_wkd,y1_wnd=[],[]
y2_wkd,y2_wnd=[],[]
for j,dmv in enumerate(sum_T[0]):
 if (dmv.isoweekday() <= 5):
  tmx_wkd.append(dmv)  
  y1_wkd.append(sum_T[1][j])
  y2_wkd.append(sum_T[2][j])
 else :
  tmx_wnd.append(dmv)  
  y1_wnd.append(sum_T[1][j])
  y2_wnd.append(sum_T[2][j])
# print jt[0].isoformat(' '),jt[1],jt[2] 
print sum(sum_T[1])/len(sum_T[1]),sum(sum_T[2])/len(sum_T[2]),len(sum_T[1]),len(sum_T[2])
fig=plt.figure(figsize=(10,8))
ax1=fig.add_subplot(3,1,1)
ax2=fig.add_subplot(3,1,3)
fig_wnd=plt.figure()
ax1_wnd=fig_wnd.add_subplot(1,1,1)
ax1.plot(tmx_wkd,y1_wkd, label="Entry")
ax1.plot(tmx_wkd,y2_wkd,label="Exit")
ax1.set_xticklabels(["M","Tu","W", "Th","F"])
wkd=[]
for j in range(7,12):
 dt=datetime.time(12,00,00)
 dd=datetime.date(2013,01,j)
 wkd.append(datetime.datetime.combine(dd,dt))
ax1.set_xticks(wkd)
ax1.set_xlabel("Day of Week")
fig.suptitle("Entry and Exit at " +rn + '(Lines-'+ lns+ ')'+ ': Weekdays')
ax1.set_title("Number of people entering and exiting subway stop every 4 hours (Weekdays)")
ax1.legend(loc=0,prop={'size':8})
wed=[]
for j in sum_EE :
 if j[0].isoweekday()==3: wed.append(j)
twed=transpose(wed)
ax2.plot(twed[0][:],twed[1][:],label="Entry")
ax2.plot(twed[0][:],twed[2][:],label="Exit")
ax2.xaxis.set_major_formatter(DateFormatter("%H:%M"))
ax2.xaxis.set_major_locator(HourLocator(interval=4))
ax2.set_title("Number of people entering and exiting subway stop every 4 hours (Wednesday)")
ax2.legend(loc=0,prop={'size':8})
fn1='./plot/' + rn[:8] + '-WKD'+'.png'
fn2='./plot/' + rn[:8] + '-WND'+'.png'
fig.savefig(fn1)
fig_wnd.suptitle("Entry and Exit at " +rn + '(Lines-'+ lns+ ')'+ ': Weekends')
ax1_wnd.plot(tmx_wnd,y1_wnd, label="Entry")
ax1_wnd.plot(tmx_wnd,y2_wnd, label="Exit")
ax1_wnd.set_title("Number of people entering and exiting subway stop every 4 hours (Weekends)")
ax1_wnd.xaxis.set_major_formatter(DateFormatter("%H:%M"))
ax1_wnd.xaxis.set_major_locator(HourLocator(interval=6))
ax1_wnd.legend(loc=0,prop={'size':8})
fig_wnd.savefig(fn2)
plt.show()


