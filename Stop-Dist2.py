import shapefile
import pyproj
import csv
def quad_det(x,y):
	if x >= 0:
	  if y>=0 : return 0
	  else : return 3
	else:
	  if y>=0: return 1
	  else : return 2     
    
def PiP(nam,num,pol,x,y):
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
              if (nam.startswith("Ble") and str(num)=='5'): print quad,quad_p  
          elif (quad-quad_p)%4 ==3:
              q_count-=1
              if (nam.startswith("Ble") and str(num)=='5'): print quad,quad_p
          elif (quad - quad_p)%4 ==2:
              det=False
              if (nam.startswith("Ble") and str(num)=='5'): print quad  
              while (det==False):
                 r= rand()
                 p_x =dx_p + r*(dx-dx_p)
                 p_y = dy_p + r*(dy-dy_p)
                 quad_m = quad_det(p_x,p_y)
                 #print quad_m,q_count,
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

def geom(ngon):
   x,y=zip(*ngon)   
   plot(x,y)  
f1=open("./MTA Feeds/stops.txt")
#f2=open("Sixth-Dist","wb")
#f3=open("UnId-Stops.csv","wb")
lats,lons,name=[],[],[]
#cs_wst =csv.writer(f3)
cs_readstops = csv.DictReader(f1)
for j, rec in enumerate(cs_readstops):
 if rec['location_type']=='1':
   lats.append(rec['stop_lat'])
   lons.append(rec['stop_lon'])
   name.append(rec['stop_name'])
print len(lats)
ptx=[]
pty=[]
#sf=shapefile.Reader("../../Data Science/NYC GIS/Cong-Dist/nycg")
sf=shapefile.Reader("../../Data Science/NYC GIS/Comm2/new_york_city_community_districts")
#sf=shapefile.Reader("../../Data Science/NYC GIS/Cong-Dist-S/nyscd")
#sf=shapefile.Reader("../../Data Science/NYC GIS/Neighborhood/new_york_city_neighborhoods")
shs=sf.shapes()
rcs=sf.records()
#p1=pyproj.Proj(init="epsg:3628", preserve_units=True)
p1=pyproj.Proj(init="epsg:2030")
poly=[]
#print shs[2].points[3]
for j,sh in enumerate(shs):
#   ptx,pty=[],[]
#   for pt in sh.points:
#        ptx.append(pt[0])
#        pty.append(pt[1])
#   l_x,l_y = p1(ptx,pty,inverse=True)
#   l_x=[p[0] for p in sh.points]
#   l_y=[p[1] for p in sh.points]
#   pts_ll=zip(l_x,l_y)
#   bbl_x,bbl_y=p1(sh.bbox[0],sh.bbox[1],inverse=True)   
#   bbr_x,bbr_y=p1(sh.bbox[2],sh.bbox[3],inverse=True)   
#   bb=[bbl_x,bbl_y,bbr_x,bbr_y]
   
   poly.append([rcs[j][0],sh.points,sh.bbox])
neigh=[]
s=0
for pt in zip(name,lons,lats):
  det=False
  for pol in poly:
   #  if(not pol[0].startswith("park_cem")):
	    #if pol[0].startswith("Lower"):
	#	 geom(pol[1])
	    if(float(pt[1])>=pol[2][0] and float(pt[1])<=pol[2][2] and float(pt[2])>=pol[2][1] and float(pt[2])<=pol[2][3]): 
		  if PiP(pt[0],pol[0],pol[1],float(pt[1]),float(pt[2])):
			  det=True
			  pol.append(pt[0])
	#		  if pol[0].startswith("Lower"):
	#		     scatter(float(pt[1]),float(pt[2]),marker='s')
  if det==False: 
    print [pt[0],pt[1],pt[2]]  
    s=s+1
print s
s=0
for j,pol in enumerate(poly):
 neigh.append([float(len(pol)-3)/rcs[j][1],len(pol)-3,pol[0]])
 s+= len(pol)-3
print s
neigh.sort()
for n in neigh:
 print n[1],n[2]
