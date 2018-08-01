import json
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

fRead=open('world_cup.json','r')
data= json.loads(fRead.read())
fRead.close()

winners={"Draw":0}
for line in data:
    line[1]=str(line[1])
    line[2]=str(line[2])
    line[3]=int(line[3])
    line[4]=int(line[4])

for line in data:
    if line[3]>line[4]:
        if line[1] not in winners.keys():
            winners[line[1]]=1
        else:
            winners[line[1]]+=1
    elif line[3]<line[4]:
        if line[2] not in winners.keys():
            winners[line[2]]=1
        else:
            winners[line[2]]+=1
    else:
        winners['Draw']+=1

bdict = {(value,key):key for (key,value) in winners.items()}
t=list(bdict.items())
t.sort(reverse=True)
for item in t:
    print item[0]

