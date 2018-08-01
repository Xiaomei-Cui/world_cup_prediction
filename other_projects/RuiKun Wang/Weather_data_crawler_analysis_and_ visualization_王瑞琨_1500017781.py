
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import json
appcode = '09195d33473c4f249577430f24b69f27'
def get_df(areaid, areaname_dict, month, appcode):
    url = 'https://ali-weather.showapi.com/weatherhistory'
    payload = {'areaid': areaid, 'month': month}
    headers = {'Authorization': 'APPCODE {}'.format(appcode)}
    r = requests.get(url, params=payload, headers=headers)
    content_json = json.loads(r.content)
    df = pd.DataFrame(content_json['showapi_res_body']['list'])
    df['areaname'] = areaname_dict[areaid]
    return df
def get_dfs(areaname_dict, months, appcode):
    dfs = []
    for areaid in areaname_dict:
        dfs_times = []
        for month in months:
            temp_df = get_df(areaid, areaname_dict, month, appcode)
            dfs_times.append(temp_df)
        area_df = pd.concat(dfs_times)
        dfs.append(area_df)
    return dfs
areaname_dict = {'101010100':'北京','101020100':'上海','101280601':'深圳','101291401':'丽江'}
months = ['201801','201802','201803','201804','201805','201806','201807']
dfs = get_dfs(areaname_dict, months, appcode)
df = pd.concat(dfs)
df


# In[ ]:


#将日期和aqi转为需要的格式
df.time = pd.to_datetime(df.time)
df.aqi = pd.to_numeric(df.aqi)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotnine
from plotnine import *
from mizani.breaks import date_breaks
#比较api空气状况折线图
(ggplot(df, aes(x='time', y='aqi', color='factor(areaname)')) + geom_line() +
 scale_x_datetime(breaks=date_breaks('2 week')) +
 xlab('日期') +
 theme_matplotlib() +
 theme(axis_text_x=element_text(rotation=45, hjust=1)) +
 theme(text=element_text(family='Arial Unicode MS'))
 )


# In[ ]:


#比较aqiLevel散点图
(ggplot(df, aes(x='time', y='aqiLevel', color='factor(areaname)')) + geom_point() +
 scale_x_datetime(breaks=date_breaks('2 week'))+
 xlab('日期') +
 theme_matplotlib() +
 theme(axis_text_x=element_text(rotation=45, hjust=1)) +
 theme(text=element_text(family='Arial Unicode MS'))
 )

