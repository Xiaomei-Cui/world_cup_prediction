import requests
from lxml import etree
import pandas as pd
import time
import random

name, score, comment = [], [], []

def danye_crawl(page):
    url = 'https://movie.douban.com/subject/26752088/comments?start={}&limit=20&sort=new_score&status=P&percent_type='.format(page*20)
    response = requests.get(url)
    response = etree.HTML(response.content.decode('utf-8'))
    if requests.get(url).status_code == 200:
        print( '第{}页爬取成功'.format(page))
    else:
        print( '第{}页爬取失败'.format(page))

    for i in range(1,21):
        name_list = response.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a'.format(i))
        score_list = response.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[2]'.format(i))
        comment_list = response.xpath('//*[@id="comments"]/div[{}]/div[2]/p/span'.format(i))

        name_element = name_list[0].text
        score_element = score_list[0].attrib['class'][7]
        comment_element = comment_list[0].text

        name.append(name_element)
        score.append(score_element)
        comment.append(comment_element)

for i in range(11):
    danye_crawl(i)
    time.sleep(random.uniform(6, 9))

res = {'name':name, 'score':score, 'comment':comment}
res = pd.DataFrame(res, columns = ['name','score','comment'])
res.to_csv("douban.csv")

with open('comment.txt','w',encoding='GB18030',errors='ignore')as f:
    for text in comment:
        f.write(text+'\n')
