import requests
pass_ticket='xRssWVn3NIHMBNXllviqxirzgLofsQxhw3ufPyyVoFWA0xO%2BgfVWOrQ6Kjfery9m'
key='e155f595f10ac74c32383b88b69eb1ad8d3659e650162415ad68c8dcbca1a39939eea40f8c7dce9ed8112b045757e34120a2ac39047bc087111dce0288ba778dd8027ab322c76cd6c81c16fcb9df803a'
openid='owanlsiBXzvBkUypZ7BSRUdFuBeU'
url='https://game.weixin.qq.com/cgi-bin/gamewap/getuserheroperformance?zone_area_id=3174&hero_id=127&openid='+openid+'&uin=&key=&pass_ticket='+pass_ticket
cookie='''sd_userid=4071530372494441; sd_cookie_crttime=1530372494441; pgv_pvid=2339141787; pgv_info=ssid=s5304679219; qv_als=A4gcSKjK6mBr3SfiA11531534126NEW8Zw==; httponly; uin=MzM0OTE1OTY5OQ%3D%3D; key='''+key+'; pass_ticket='+pass_ticket
header={
    'Host':'game.weixin.qq.com',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Linux; Android 8.0; BKL-AL20 Build/HUAWEIBKL-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
    'Accept':'*/*',
    'Referer':'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/hero.html?hero_id=127&openid='+openid+'&zone_area_id=3174&ssid=1021&uin=&key=&pass_ticket='+pass_ticket+'&abtest_cookie=BAABAAgACgALAAwABwCfhh4APoseACSXHgD2lx4AyJgeAPSYHgD6mB4AAAA%3D&wx_header=1',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
    'Cookie':cookie,
    'X-Requested-With':'com.tencent.mm',
    'Q-UA2':'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044109&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL20 &RL=1080*2160&OS=8.0.0&API=26',
    'Q-GUID':'7b964e09fb9ce102a95ea3db13b788cb',
    'Q-Auth':'31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'
}
r=requests.get(url,headers=header,timeout=5)
temp=r.json()
print(temp)