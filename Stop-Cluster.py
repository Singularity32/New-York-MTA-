import csv
from mpl_toolkits.basemap import Basemap
clust_num=4;
def dist(a,b):
   return 100000.0*sqrt(pow(a/100000.0,2)+pow(b/100000.0,2))
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
bbox=[-74.02,40.91,-73.71,40.54]
x_g=(bbox[2]-bbox[0])*rand(clust_num) + bbox[0];
y_g=(bbox[3]-bbox[1])*rand(clust_num) + bbox[1];
clus_stop = [[] for j in range(0,clust_num)]
stop_clus=[int(rand()*clust_num) for j in enumerate(lats)]
err=2
ct=0
m=Basemap(projection='lcc', llcrnrlon=-74.31,llcrnrlat=40.47,urcrnrlon=-73.63,urcrnrlat=40.92,lon_0=-73.981,lat_0=40.758,resolution='h')
m_st=m.drawstates()
m_cl=m.drawcoastlines()
lons_x,lats_y=m(lons,lats)
x,y=m(x_g,y_g)
print x,y
while (err>0.01 and ct <200) :
  ct+=1
  err=0
  for j,pos in enumerate(zip(lons_x,lats_y)):
     d_clus=[dist(pos[0]-x1,pos[1]-y1) for x1,y1 in zip(x,y)]
     err=err+ min(d_clus)
     re_clus=d_clus.index(min(d_clus))     
     if ct<2:
       stop_clus[j]=re_clus
       clus_stop[stop_clus[j]].append(j)
     elif (re_clus!=stop_clus[j]):
         clus_stop[stop_clus[j]].remove(j)
         clus_stop[re_clus].append(j)
         stop_clus[j]=re_clus
         #print j
  for j,pos in enumerate(zip(x,y)):
      d_x=[lons_x[k] for k in clus_stop[j]]   
      d_y=[lats_y[k] for k in clus_stop[j]]
      x_n=sum(d_x)/len(d_x)   
      y_n=sum(d_y)/len(d_y)   
      x[j]=x_n
      y[j]=y_n
print err
if clust_num==4:
   co_set=['r','b','g','y']
else:
   co_set=[(rand(),rand(),rand()) for j in range(clust_num)]
for x1,y1,stp in zip(x,y,clus_stop):
  print x1,y1,len(stp) 
  z= [name[k] for k in stp[0:-1:10]]
  print z
co_ar=[]
for j, n in enumerate(name):
  co_ar.append(co_set[stop_clus[j]])
#scatter(x,y,color='m')
scatter(lons_x, lats_y,c=co_ar,marker='h', s=20)
scatter(x,y,c='k', marker='*',s=70)
for j,pos in enumerate(zip(x,y)):
 annotate(str(len(clus_stop[j])),xy=(pos[0],pos[1]),size='medium')
nm="./plot/Cluster-"+str(clust_num)+"-stops.png"
#savefig(nm)   
#sf=shapefile.Reader("../../Data Science/NYC GIS/Cong-Dist/nycg")
