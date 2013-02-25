import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
f1=open("./MTA Feeds/stops.txt")
f2=open("Stop_GeoJson.json","wb")
cs_readstops = csv.DictReader(f1)
GeoJson_FC='{ "type" : "FeatureCollection, "features": ['
for rec in cs_readstops:
  if (len(rec['stop_id'])==3):
    GeoJson_pt = '{ "type": "Point", "coordinates":' + '['+rec['stop_lon']+','+rec['stop_lat'] + ']' + '}'
    GeoJson_Feature = '{ "type" : "Feature", "geometry":'+ GeoJson_pt+ ', "properties": { "name":' + '"'+rec['stop_name'] +'"'+ '}}'   
    GeoJson_FC= GeoJson_FC+GeoJson_Feature + ',' 
GeoJson_FC=GeoJson_FC.rstrip(',')+ ']}'
f2.write(GeoJson_FC)
