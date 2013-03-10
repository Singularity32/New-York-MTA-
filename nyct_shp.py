# This file determines the ranks of neighborhoods based on the number of subway stops per unit area. 
from scipy.optimize import curve_fit
import shapefile
import pyproj
import csv
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
# Determining the quadrant of a vector
def quad_det(x,y):
	if x >= 0:
	  if y>=0 : return 0
	  else : return 3
	else:
	  if y>=0: return 1
	  else : return 2     
# Determining if a point is in a polygon    
def PiP(pol,x,y):
   q_count,quad_p=0,-1
   quad=0
   for ps in pol:
       dx=ps[0]-x
       dy=ps[1]-y
       if dx==0 or dy==0: return True
       quad =quad_det(dx,dy)
       if (quad_p >=0):
          if (quad-quad_p)%4 ==1:
              q_count+= 1
          elif (quad-quad_p)%4 ==3:
              q_count-=1
          elif (quad - quad_p)%4 ==2:  # Here we have to determine if the quadrant changed in a clockwise or ant-clockwise direction.
              det=False
              while (det==False):      # Choose a point on the line joining the two vectors
                 r= rand()
                 p_x =dx_p + r*(dx-dx_p)
                 p_y = dy_p + r*(dy-dy_p)
                 quad_m = quad_det(p_x,p_y)
                 if (quad_m!=quad) and (quad_m!=quad_p) :
                       if (quad_m -quad_p)%4==1:
                         q_count+=2          
                       else:
                         q_count-=2          
                       det=True  
       dx_p=dx
       dy_p=dy
       quad_p=quad        
   if abs(q_count)==4:
       return True
   else:
       return False

def geom(ngon,name,co):
 lons,lats=zip(*ngon)
 x,y=m(lons,lats)
 #print name, x[10],y[10]
 pol=zip(x,y)
 poly=Polygon(pol,label=name,fill=True,color=cm.OrRd(co))
 plt.gca().add_patch(poly)
 return poly   
f1=open("./MTA Feeds/stops.txt")
#f3=open("UnId-Stops.csv","wb")
lats,lons,name=[],[],[]
#cs_wst =csv.writer(f3)
cs_readstops = csv.DictReader(f1)


for j, rec in enumerate(cs_readstops):
 if rec['location_type']=='1':
   lats.append(rec['stop_lat'])
   lons.append(rec['stop_lon'])
   name.append(rec['stop_name'])


ptx=[]
pty=[]
# Shapefile for the neighborhoods
sf=shapefile.Reader("../../Data Science/NYC GIS/nyct2010/nyct2010")
shs=sf.shapes()
rcs=sf.records()

m=Basemap(projection='lcc', llcrnrlon=-74.31,llcrnrlat=40.47,urcrnrlon=-73.63,urcrnrlat=40.92,lon_0=-73.981,lat_0=40.758,resolution='h')
m_st=m.drawstates()
m_cl=m.drawcoastlines()

f5=open("bb","wb")

pj=pyproj.Proj(init="epsg:3628",preserve_units=True)
Rect=[]
poly=[]
for j,sh in enumerate(shs):
   x,y=zip(*sh.points)
   x_l,y_l=pj(x,y,inverse=True)
   rec_poly=zip(x_l,y_l)   
   bb_x,bb_y=zip(*reshape(sh.bbox,(2,2)))
   bb_lat,bb_lon=pj(bb_x,bb_y,inverse=True)
   bbox=reshape(zip(bb_lat,bb_lon),4)  
   f5.writelines([str(bbox)])
   poly.append([rcs[j][7],rec_poly,bbox])
   x_l,y_l = m(bbox[0],bbox[1])
   x_r,y_r = m(bbox[2],bbox[3])
   Rect.append(Rectangle((x_l,y_l),x_r-x_l,y_r-y_l))
neigh=[]
s=0
s2=[0,0,0,0,0]

for pt in zip(name,lons,lats):
  det=False
  det_bb=False
  for j,pol in enumerate(poly):
        if (not pol[0].startswith("park")): 
       # Determine if the point is inside the bounding box of the neighborhood shape
	    if(float(pt[1])>=pol[2][0] and float(pt[1])<=pol[2][2] and float(pt[2])>=pol[2][1] and float(pt[2])<=pol[2][3]): 
                  det_bb=True
		  if PiP(pol[1],float(pt[1]),float(pt[2])):
			  det=True
			  pol.append(pt[0])
                          if rcs[j][1].startswith("Sta"):
                                 s2[0]+=1
                          if rcs[j][1].startswith("The"):
                                 s2[1]+=1
                          if rcs[j][1].startswith("Quee"):
                                 s2[2]+=1
                          if rcs[j][1].startswith("Broo"):
                                 s2[3]+=1
                          if rcs[j][1].startswith("Man"):
                                 s2[4]+=1
            
  if det==False: 
    if det_bb==True:
      for j,pol in enumerate(poly):
         if (not pol[0].startswith("park")): 
       # Determine if the point is inside the bounding box of the neighborhood shape
	    if(float(pt[1])>=pol[2][0] and float(pt[1])<=pol[2][2] and float(pt[2])>=pol[2][1] and float(pt[2])<=pol[2][3]): 
			  pol.append(pt[0])
                          print pt[0],pol[0]
    else:s=s+1
print s

print "Number of stops in each borough", s2
s=0
for j,pol in enumerate(poly):
 neigh.append([float(len(pol)-3),len(pol)-3,pol[0],pol[1]])
 s+= len(pol)-3
print s
neigh.sort()
for nb in neigh[-1:-10:-1]:
 print nb[1],nb[2]
neigh.sort(key=lambda x:x[1])
star_Co=[]
pgon=[]
for j,nb in enumerate(neigh):
 if (not nb[2].startswith("park_cem")):
    star_Co.append(nb[1]*1.0/neigh[-1][1])
    if nb[1]<0: print nb[1],nb[2]
    pgon.append(geom(nb[3],nb[2],star_Co[-1]))
an=[]
for j,sh in enumerate(shs):
    at=annotate(str(rcs[j][7])+ '\n'+str(len(poly[j])-3),xy=m((bbox[0] + bbox[2])/2,(bbox[1] + bbox[3])/2),size='medium',visible=False)   
    an.append(at)
#imshow(Star_Co,cmap=cm.OrRd)
#colorbar()
#plt.savefig("Stop-Color.png")

def onclick(event):
    for j,R in enumerate(Rect): 
                if (event.xdata > R.get_x() and event.xdata < (R.get_x() +R.get_width()) and event.ydata > R.get_y() and event.ydata < (R.get_y() +R.get_height())):
                  print "Yes"
                  an[j].set_visible(True)      
                  plt.show()
                else:
                   an[j].set_visible(False)

cid = gcf().canvas.mpl_connect('button_press_event', onclick)
x=[l[0] for l in neigh]
fig=figure(figsize=(8,6))
fig.suptitle("Distribution of subway stops/unit area across the 193 neighborhoods of NYC")
ax=fig.add_subplot(2,1,1)
ax.set_title("Histogram fit to power law")
h=ax.hist(x,22)
ax2=fig.add_subplot(2,1,2)
ax2.set_title("Histogram fit to exponential distribution")
ax2.hist(x,22)
x= (h[1][:-1] +h[1][1:])/2
y=h[0]
def f(x1,a,alpha):
    return a*pow(x1,alpha)

popt,pcov =curve_fit(f,x,y)
print popt,pcov
ax.plot(x,f(x,popt[0],popt[1]),label='~1/x')
ax.legend()
def f2(x1,a,alpha):
    return a*exp(alpha*x1)
popt,pcov =curve_fit(f2,x,y)
print popt,pcov
ax2.plot(x,f2(x,popt[0],popt[1]),label='Exp['+format(popt[1],'e')+']')
ax2.legend()
fig.savefig("./plot/Sub-Neigh-Dist.png")
neigh.sort(key=lambda x :x[1])
f3=open("Neighborhood-Stops","wb")
[f3.write('    ' + str(n[1]) + '    '+n[2]+'\n ') for n in neigh]
s=0
cdist=[]
for j,ln in enumerate(neigh):
   s=s+ln[1]
   cdist.append(s)
fig2=figure()
x=[i*(100.0)/len(neigh) for i in range(0,len(neigh))]
plot(x,cdist)
xv_half=[50,50]
yv_half=[0,cdist[len(neigh)/2]]
xh_half=[0,50]
yh_half=[cdist[len(neigh)/2],cdist[len(neigh)/2]]
plot(xv_half,yv_half,'r--')
plot(xh_half,yh_half,'r--')
xv_tq=[75,75]
yv_tq=[0,cdist[3*len(neigh)/4]]
xh_tq=[0,75]
yh_tq=[cdist[3*len(neigh)/4],cdist[3*len(neigh)/4]]
plot(xv_tq,yv_tq,'r--')
plot(xh_tq,yh_tq,'r--')
xlabel("%Neighborhoods")
fig2.suptitle("Cumulative distribution of stops")
fig2.savefig("./plot/Cumulative-NS.png") 
close(fig)
close(fig2)
