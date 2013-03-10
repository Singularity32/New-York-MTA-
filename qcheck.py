import csv
f1=open("./Turnstile/Turnstile-Data.txt","rb")
f2=open("./Turnstile/RBS.csv","rb")
f3=open("./Turnstile/Stop-EntExt.csv","wb")
r_dat=csv.reader(f1)
r_rbs=csv.reader(f2)
r_EE=csv.writer(f3)
t_ent,t_ext=0,0
pent,pext=0,0
#print len(r_rbs)
SCP=""
for rbs in r_rbs:
	T_ent=0
	T_ext=0
        if len(rbs) < 5: break
        name=rbs[2]
#        print name
        f1.seek(0)
	tent,text=0,0
	for rec in r_dat:
		  if rec[0]==rbs[1] and rec[1]==rbs[0]:
			 if (pent==0 or rec[2]!=SCP):
				  pent =int(rec[6])
				  pext=int(rec[7])
				  SCP=rec[2]
			 for j in range(3,len(rec),5):
				  dent=int(rec[j+3]) - pent
				  dext=int(rec[j+4]) - pext
				  pent=int(rec[j+3])
				  pext=int(rec[j+4])
				  t_ent =t_ent +dent      
				  t_ext=t_ext+dext
		  T_ent+=t_ent/7
		  T_ext+=t_ext/7
        r_EE.writerow([name,str(T_ent),str(T_ext)])
