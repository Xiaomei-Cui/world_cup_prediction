import csv

fRead=open('used country.txt','r')
countries=[]
for line in fRead.readlines():
    line=line.strip()
    countries.append(line.split(' ',1)[-1])
fRead.close()

data=list(csv.reader(open("GDP.csv")))
already=[]
for line in data:
    if line[1] in countries:
        already.append(line)
print len(already)

csvFile2 = open('GDP in cup.csv','wb')
writer = csv.writer(csvFile2)
for line in already:
    writer.writerow(line)
csvFile2.close()
'''
Czechoslovakia 捷克斯洛伐克，1992解体为捷克、斯洛伐克 1990最后五场比赛，而最古老的GDP数据日期为1990
German DR 民主德国 1990和联邦德国合并为德国 仅在1974年出现在六场比赛中（其中一场为与联邦德国） GDP中德国从1970年开始存在数据
Russia 苏联？俄罗斯联邦？都叫Russia
Yugoslavia 南斯拉夫，2006年解体 进过不少比赛，但没有合适的GDP数据
England 英格兰？英国？ 英国历来派出四个队伍参赛，GDP数据可四个队共用英国的？
Northern Ireland 英国的政治实体之一
Scotland 英国政治实体之一
Wales 英国的政治实体之一
'''
