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

def geom(ngon,inc,co):
 p=Polygon(ngon,label=str(inc),fill=True,color=cm.OrRd(co))
 plt.gca().add_patch(p)
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
sf_A=shapefile.Reader("../../Data Science/NYC GIS/nyct2010A/median_income_nys")
shs=sf_A.shapes()

m=Basemap(projection='lcc', llcrnrlon=-74.31,llcrnrlat=40.47,urcrnrlon=-73.63,urcrnrlat=40.92,lon_0=-73.981,lat_0=40.758,resolution='h')
m_st=m.drawstates()
m_cl=m.drawcoastlines()

f5=open("bb","wb")

pj=pyproj.Proj(init="epsg:3628",preserve_units=True)
Rect=[]
poly=[]
ny_c="New York County"
bk="Kings County"
qs="Queens County"
bx="Bronx County"
st="Richmond County"
s=0
for j,sh in enumerate(shs):
   try:
           tr=sf_A.record(j)[1]
           if (tr.find(ny_c)>-1 or tr.find(bk)>-1 or tr.find(qs)>-1 or tr.find(bx)>-1 or tr.find(st)>-1):
                   #if (tr.find(ny_c)>-1 and tr.find(' 21,')>-1): print sf_A.record(j)[6],sf_A.record(j)[7]
                   s=s+1
		   lons,lats=zip(*sh.points)
		   x,y=m(lons,lats)
		   #print name, x[10],y[10]
		   re_pol=zip(x,y)
		   x_l,y_l = m(sh.bbox[0],sh.bbox[1])
		   x_r,y_r = m(sh.bbox[2],sh.bbox[3])
		   poly.append([float(sf_A.record(j)[7].replace(',','')),re_pol,[x_l,y_l,x_r,y_r]])
		   Rect.append(Rectangle((x_l,y_l),x_r-x_l,y_r-y_l))
   except ValueError: 
           num=0
print s
neigh=[]
s=0
po=[j[0] for j in poly]
po.sort()
print po[-1]
star_Co=[]
#inc=[p[0] for p in poly]
#f=figure()
#ax=f.add_subplot(1,1,1)
#ax.hist(inc)
pgon=[]
for j,pol in enumerate(poly):
    star_Co =  pol[0]*1.0/po[-1]
    pgon.append(geom(pol[1],pol[0],star_Co))
an=[]
plt.show()
for j,pol in enumerate(poly):
    at=annotate(str(pol[0])+ '\n',xy=((pol[2][0] + pol[2][2])/2,(pol[2][1] + pol[2][3])/2),size='medium',visible=False)   
    an.append(at)
#imshow(Star_Co,cmap=cm.OrRd)
#colorbar()
#plt.savefig("Stop-Color.png")
fl1=open("stationWeatherDiff.csv","rb")
print "Something"
csr1=csv.DictReader(fl1)
csr2=csv.DictReader(f1)
x,y,siz,co=[],[],[],[]
for rc1 in csr1:
  f1.seek(0)
  for rc2 in csr2:
     if  rc1["Station Name"].lower()==rc2["stop_name"].lower() :
         lons,lats=m(float(rc2["stop_lon"]),float(rc2["stop_lat"]))
         x.append(lons)
         y.append(lats)
         siz.append(exp(20*abs(float(rc1["normedDiff"]))))
         if float(rc1["normedDiff"]) > 0 : 
             co.append((0.0,0,1.0))
         else:
             co.append((1.0,0,0))
   

f_s=figure()
ax=f_s.add_subplot(1,1,1)
ax.scatter(x,y,s=siz,color=co,marker='o')

def onclick(event):
    for j,pol in enumerate(poly): 
                #if (event.xdata > R.get_x() and event.xdata < (R.get_x() +R.get_width()) and event.ydata > R.get_y() and event.ydata < (R.get_y() +R.get_height())):
                if PiP(pol[1],event.xdata,event.ydata) :
                  print "Yes"
                  an[j].set_visible(True)      
                  plt.show()
                else:
                   an[j].set_visible(False)

cid = gcf().canvas.mpl_connect('button_press_event', onclick)
