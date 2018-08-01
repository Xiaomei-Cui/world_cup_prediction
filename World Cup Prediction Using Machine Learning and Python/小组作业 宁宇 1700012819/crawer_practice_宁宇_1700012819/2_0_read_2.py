# -*- coding:utf-8 -*-
# python 3.6
import json
fRead=open('2_0.txt','r',encoding='utf-8')
result=[]
temp=['','','','','','']
num=0
count=0
lst=fRead.readlines()
fRead.close()
for line in lst:
    line=line.strip()
    temp[num]=line
    num=num+1
    if num == 6:
        result.append(list(temp))
        num=0
        count=count+1
        print('%.3f'%(count*600.0/len(lst)),'%',end='\r'),
print ('load finish')
fWrite=open('2_0.json','w',encoding='utf-8')
fWrite.write(json.dumps(result))
fWrite.close()
print ('write finish')