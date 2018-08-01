import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import csv

reader=csv.reader(open('country.CSV'))
country=list(reader)
del(country[0])
d={}
for line in country:
    d[line[3]]=line[1]

outfile=open("country_data.csv",'r')
data=csv.reader(outfile)
data=list(data)
outfile.close()

for line in data:
    if line[2] in d:
        line[1]=d[line[2]]

csvFile2 = open('country_out.csv','wb')
writer = csv.writer(csvFile2)
for line in data:
    writer.writerow(line)
csvFile2.close()