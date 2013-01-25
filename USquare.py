import csv
nrs=csv.reader(open("../stop_times.txt","rb"))
f=open("../trips.txt","rb")
nrt=csv.reader(f)
nr=csv.reader(open("../stops.txt","rb"))
nw=csv.writer(open("USq-tripN.txt","wb"))
for tp in nrs:
  if ('635N'in tp[3] or 'L03N' in tp[3] or 'R20N' in tp[3]):
   f.seek(0)
   for i in nrt:
     if tp[0]==i[2]:
      # print i[0], tp[2]
       if 'WKD' in i[1]:
        nw.writerow(['WKD',i[0],tp[1]])
        break        
       elif 'SAT' in i[1]:
        nw.writerow(['SAT',i[0],tp[1]])
        break        
       elif 'SUN' in i[1]:
        nw.writerow(['SUN',i[0],tp[1]])
        break 
