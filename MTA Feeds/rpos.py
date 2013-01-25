import csv
import os,string
dir=os.path.dirname(__file__)
#filename=os.path.join(dir,'/media/DATA/MTA Feed/Tests/latlong.txt')
nr=csv.reader(open("shapes.txt","rb"))
nw=csv.writer(open("./Tests/latlong.txt",'wb'))
ct=0
for rw in nr:
 if ct==0:
  for j in rw:
    print ('lon' in j)
 ct=ct+1
 if ct<30 and ct>1:
   print rw[1],rw[2]
   nw.writerow([rw[1],rw[2]])
