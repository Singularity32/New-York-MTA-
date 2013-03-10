import csv
from datetime import timedelta
def tinsec(fm):
  fm_hr=int(fm[0])
  fm_min=int(fm[1])
  fm_sec=int(fm[2])
  return(fm_hr*3600 + fm_min*60 + fm_sec)
f1=open("USq-tripN.txt","rb")
f2=open("USq-TimeInt.txt","wb")
nw=csv.writer(f2)
nr=csv.reader(f1)
flag=0
rwp=nr.next()
prev1=rwp[2].split(':')
tpre1=tinsec(prev1)
rwp=nr.next()
prev2=rwp[2].split(':')
d=timedelta(hours=int(prev1[0]),minutes=int(prev1[1]),seconds=int(prev1[2]))
print d.seconds
tpre2=tinsec(prev2)
t_int_p=tpre2-tpre1
nw.writerow([rwp[0],rwp[1]])
nw.writerow([ prev2[0]+':'+prev2[1]+':' + prev2[2],t_int_p/60])
tpre=tpre2
print tpre
for rw in nr:
  tn=rw[2].split(':')
  tnext=tinsec(tn)
  t_int_n=(tnext-tpre)
  if (rw[0]==rwp[0] and rw[1]==rwp[1]):
   if (abs(t_int_n -t_int_p) >60):
     nw.writerow([tn[0]+':'+ tn[1]+':' +tn[2],t_int_n/60])
     t_int_p=t_int_n
  else: 
       nw.writerow([rw[0],rw[1]])
       rwp=rw
  tpre=tnext  
