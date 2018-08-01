import simplejson as json
import requests
import jsonpath

pass_ticket = '%2BjccTPYRP4OQQWt1JcT45akaZnF%2F1SxRA0SvysLBX0HfKd6i2plB79%2B4QSqoKLmb'
key = '961d6b7b3101fe37b759a3ecce817473253ecfb5c0886d76b8a98bd4ddc82e3273ddd265ee7c50c4c7a1a0d8bd17133a3611cbe2d958ff63778a9905f76599244c22abe564333297528a6cb9779c4c39'

def get_index(openid):
    url = 'https://game.weixin.qq.com/cgi-bin/gamewap/getpubgmdatacenterindex?openid=' + openid + '&uin=&key=&pass_ticket=' + pass_ticket
    cookie = '''sd_userid=4071530372494441; sd_cookie_crttime=1530372494441; pgv_pvid=2339141787; pgv_info=ssid=s5304679219; qv_als=A4gcSKjK6mBr3SfiA11531534126NEW8Zw==; httponly; uin=MzM0OTE1OTY5OQ%3D%3D; key=''' + key + '; pass_ticket=' + pass_ticket
    header = {
        'Host': 'game.weixin.qq.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL20 Build/HUAWEIBKL-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
        'Accept': '*/*',
        'Referer': 'https://game.weixin.qq.com/cgi-bin/h5/static/pubgm/index.html?openid=' + openid + '&ssid=1021&rpt_allpath=2306&abtest_cookie=BAABAAgACgALAAwACACfhh4APoseACOXHgD2lx4AyJgeAPSYHgD6mB4ABpkeAAAA&pass_ticket=' + pass_ticket + '&wx_header=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
        'Cookie': cookie,
        'X-Requested-With': 'com.tencent.mm',
        'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044113&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL20 &RL=1080*2160&OS=8.0.0&API=26',
        'Q-GUID': '7b964e09fb9ce102a95ea3db13b788cb',
        'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'
    }
    r = requests.get(url, headers=header, timeout=5)
    r.enconding = 'utf-8'
    temp=json.loads(r.text)
    print(temp)
    game_seq = jsonpath.jsonpath(temp,'$..game_seq')
    game_svr_entity = jsonpath.jsonpath(temp,'$..game_svr_entity')
    relay_svr_entity = jsonpath.jsonpath(temp,'$..relay_svr_entity')
    for i in range(0,5):
        with open('battle_list.txt','a+') as f:
            f.seek(0)
            text=f.read()
            if text.find('{} {} {}'.format(game_seq[i],game_svr_entity[i],relay_svr_entity[i]))!=-1:
                continue
            else:
                f.write('{} {} {}\n'.format(game_seq[i],game_svr_entity[i],relay_svr_entity[i]))
                print('{} {} {}\n'.format(game_seq[0], game_svr_entity[0], relay_svr_entity[0]))
                get_battle(game_seq[i],game_svr_entity[i],relay_svr_entity[i],openid)

def get_battle(game_seq,game_svr_entity,relay_svr_entity,openid):
    game_seq=str(game_seq)
    game_svr_entity = str(game_svr_entity)
    relay_svr_entity = str(relay_svr_entity)
    url = 'https://game.weixin.qq.com/cgi-bin/gamewap/getbattledetail?game_svr_entity='+game_svr_entity+'&game_seq='+game_seq+'&relay_svr_entity='+relay_svr_entity+'&openid=' + openid + '&uin=&key=&pass_ticket=' + pass_ticket
    cookie = '''sd_userid=4071530372494441; sd_cookie_crttime=1530372494441; pgv_pvid=2339141787; pgv_info=ssid=s5304679219; qv_als=A4gcSKjK6mBr3SfiA11531534126NEW8Zw==; httponly; uin=MzM0OTE1OTY5OQ%3D%3D; key=''' + key + '; pass_ticket=' + pass_ticket
    header = {
        'Host': 'game.weixin.qq.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL20 Build/HUAWEIBKL-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
        'Accept': '*/*',
        'Referer': 'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/index.html?game_svr_entity=71548&game_seq=1532005684&relay_svr_entity=504169056&openid=' + openid + '&zone_area_id=3174&ssid=1024&uin=&key=&pass_ticket=' + pass_ticket + '&abtest_cookie=BAABAAgACgALAAwABwCfhh4APoseACSXHgD2lx4AyJgeAPSYHgD6mB4AAAA%3D&wx_header=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
        'Cookie': cookie,
        'X-Requested-With': 'com.tencent.mm',
        'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044109&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL20 &RL=1080*2160&OS=8.0.0&API=26',
        'Q-GUID': '7b964e09fb9ce102a95ea3db13b788cb',
        'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'
    }
    r = requests.get(url, headers=header, timeout=5)
    r.enconding = 'utf-8'
    '''
    with open('{}_{}_{}.txt'.format(game_seq,game_svr_entity,relay_svr_entity),'w') as f:
        f.write(r.text)
        '''
    temp = json.loads(r.text)
    print(temp)
    openid = jsonpath.jsonpath(temp, '$..open_id')
    print(openid)
    with open('openid.txt','a+') as f:
        f.seek(0)
        text=f.read()
        for i in range(0,len(openid)):
            if text.find('{}'.format(openid[i]))!=-1:
                continue
            else:
                f.write('{}\n'.format(openid[i]))
                get_index(openid[i])
    print(openid)

get_index('oODfo0uCHOziKjgaDbEm-nJWNCKs')