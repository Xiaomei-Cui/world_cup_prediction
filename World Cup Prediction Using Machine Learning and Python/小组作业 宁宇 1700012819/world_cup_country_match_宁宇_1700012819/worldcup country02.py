import csv

fRead=open('used country.txt','r')
countries=[]
for line in fRead.readlines():
    line=line.strip()
    countries.append(line.split(' ',1)[-1])
fRead.close()

data=list(csv.reader(open("country_out.csv")))
already=[]
for line in data:
    if line[1]!='':
        already.append(line[1])

for item in countries:
    if item not in already:
        print item
'''
Czechoslovakia 捷克斯洛伐克，1992解体为捷克、斯洛伐克
England 英格兰？英国？
German DR 民主德国 1990和联邦德国合并为德国
Korea DPR（196） 
Korea Republic（129）
Northern Ireland 英国的政治实体之一
Russia 苏联？俄罗斯联邦？
USA（254）
Wales 英国的政治实体之一
Yugoslavia 南斯拉夫，2006年解体 
Bosnia-Herzegovina（27）
Congo DR（46）
Iran（115）
Ivory Coast（44）
Scotland 英国政治实体之一
'''