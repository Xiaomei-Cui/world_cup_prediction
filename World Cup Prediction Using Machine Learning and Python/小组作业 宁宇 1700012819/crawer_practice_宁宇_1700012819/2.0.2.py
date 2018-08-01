# -*- coding:utf-8 -*-
#python 2.7.15
import re
import requests
from bs4 import BeautifulSoup
import lxml
try:
    import openpyxl
except:
    import openpyxl
import traceback
from time import sleep
from time import time
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

def FormCrawler(url):
#    print url
#    return 1
    try:
        total=0
        for yearNum in range(2016,2019):
            tTime=time()
            maxTrytime=0
            itemNum=0
            while 1:
                turl='https://gaokao.chsi.com.cn'+url+'&start='+str(itemNum)+'&mdgsCurYear='+str(yearNum)
    #            print turl
                trytime=0;
                while 1:
                    r=requests.get(turl)
        #            sleep(0.5)
                    s=BeautifulSoup(r.text,'lxml')
                    if not s.find('title').string==u'访问错误':
        #                sleep(1)
                        break
                    print trytime,
                    trytime+=1
                    if trytime>maxTrytime: maxTrytime=trytime
                    if trytime>100: 
                        raw_input('trytimes:'+str(trytime))
                        trytime=0
                temp=s.find_all('tr')[1:]
                if not temp: break
    #            print s.prettify().encode('gbk', 'ignore')
                total=re.findall(r'&nbsp;&nbsp;. (.+?) ...&nbsp;&nbsp',r.text)[-1]
                for line in temp:
    #                    print>>fWrite,str(line).decode('utf-8')
                    record=[]
                    record.append(yearNum)
                    for item in line.find_all('td'):
    #                            print>>fWrite, item.string
                        record.append(item.string)
                    record.append(name)
                    for item in record: print>>fWrite, item
                    itemNum=itemNum+1
                    sheet.append(record)
    #                    itemNum=itemNum+30
                sys.stdout.write('\r')
                print name,str(yearNum),str(itemNum)+'/'+total,'%.2f%%'%(itemNum*100.0/float(total)),
            global sum
            sum=sum+itemNum
            t=time()
            stime=float(t-startTime)
            sstime=float(t-tTime)
            sys.stdout.write('\r')
            print name,str(yearNum),'success!!',str(itemNum)+'/'+total,sum,maxTrytime,
            print '%.2fs in %.1fs, %.3fs per 100 lines'%(sstime,stime,sstime/itemNum*100)
#            book.save("2_0_t.xlsx")
        return True

    except Exception,e:
        print
#        print s.prettify().encode('gbk', 'ignore')
        print traceback.print_exc()
        print name,'fail!'
        return False

startTime=time()

fWrite=open("2_0.txt",'w')

book=openpyxl.Workbook()
sheet=book.create_sheet()
sheet.title='2018'
sheet.append([u'年份',u'姓名',u'性别',u'就读学校',u'报名所在地',u'报考学校'])

response=requests.get('https://gaokao.chsi.com.cn/zzbm/mdgs/orgs.action?lx=1')
soup=BeautifulSoup(response.text, 'lxml')

sum=0
for line in soup.find_all('a'): 
#    print>>fWrite,url.get('href')
    url=line.get('href')
    name=line.string
    if "detail" in url:
        FormCrawler(url)
        continue
    elif "subOrgs" in url:
        url='https://gaokao.chsi.com.cn'+url
        rr=requests.get(url)
        ss=BeautifulSoup(rr.text,'lxml')
        for ll in ss.find_all('a'):
            url=ll.get('href')
            name=ll.string
            if "detail" in url:
                FormCrawler(url)
fWrite.close()
book.save("2_0.xlsx")
book.close()
print 'finish',sum