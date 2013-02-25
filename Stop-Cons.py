import csv
f1=open("./MTA Feeds/stops.txt")
#f2=open("Sixth-Dist","wb")
#f3=open("UnId-Stops.csv","wb")
lats,lons,name=[],[],[]
#cs_wst =csv.writer(f3)
cs_readstops = csv.DictReader(f1)
for j, rec in enumerate(cs_readstops):
 if rec['location_type']=='1':
   lats.append(float(rec['stop_lat']))
   lons.append(float(rec['stop_lon']))
   name.append(rec['stop_name'])
print len(lats)
bbox=[-74.02,40.91,-73.71,40.54]
x=(bbox[2]-bbox[0])*rand(clust_num) + bbox[0];
y=(bbox[3]-bbox[1])*rand(clust_num) + bbox[1];
f1=open("./Turnstile/Turnstile-Data.txt","rb")
rt=csv.reader(f1)
f3=open("./MTA Feeds/stop_EE.txt","w")
rw=csv.DictWriter(f3)
tent,text=0,0
pent,pext=0,0
for rec in rt:
  if rec[0]=='N318' and rec[1]=='R298':
         if (pent==0 or rec[2]!=SCP):
          pent =int(rec[6])
          pext=int(rec[7])
          SCP=rec[2]
         for j in range(3,len(rec),5):
            dent=int(rec[j+3]) - pent
            dext=int(rec[j+4]) - pext
            pent=int(rec[j+3])
            pext=int(rec[j+4])
            tent =tent +dent      
            text=text+dext
print tent/42,text/42
