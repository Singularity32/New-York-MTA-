import csv
nrs=csv.reader(open("../stop_times.txt","rb"))
f=open("../trips.txt","rb")
nrt=csv.reader(f)
nr=csv.reader(open("../stops.txt","rb"))
nw=csv.writer(open("USq-tripN.txt","wb"))



for tp in nrs:           # looping over every record in stop-times
  if ('635N'in tp[3] or 'L03N' in tp[3] or 'R20N' in tp[3]): # if the stop-id matches that of Union Square
	   f.seek(0)
	   for i in nrt: # looping over the trips records.
	     if tp[0]==i[2]:    # Locates the record corresponding to the trip in tp. 
	      # Writes to a file, the category of service (WKD, SAT, SUN) THE LINE NUMBER, AND THE STOP TIME
	       if 'WKD' in i[1]:
		nw.writerow(['WKD',i[0],tp[1]])
		break        
	       elif 'SAT' in i[1]:
		nw.writerow(['SAT',i[0],tp[1]])
		break        
	       elif 'SUN' in i[1]:
		nw.writerow(['SUN',i[0],tp[1]])
		break 
