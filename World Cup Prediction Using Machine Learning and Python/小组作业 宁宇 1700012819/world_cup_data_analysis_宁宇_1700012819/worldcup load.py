import sys,json
fRead=open("data_world_cup.txt",'r')
fRead.readline()
res=[]
data=fRead.readlines()
fRead.close()
sum=len(data)
num=0
print sum
for line in data:
    line=line.strip()
    lst=line.split(',')
    res.append(lst)
    num+=1
    print('%.3f%%'%(num*100.0/sum)),
    sys.stdout.write('\r')
fWrite=open("world_cup.json",'w')
fWrite.write(json.dumps(res))
fWrite.close()
print "finish!!!"
