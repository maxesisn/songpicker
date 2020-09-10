import os
from requests import cookies
from hoshino import Service
import requests
import json

sv = Service("点歌")

COMMENTS_LIMIT=3

@sv.on_prefix("点歌")
async def pick_song(bot, ev):
    song_name = ev.message.extract_plain_text()
    if not song_name:
        await bot.send(ev, "要加上歌曲名才能点歌！")
        return
    cookie = login()
    song_id=get_songid(song_name=song_name,cookie=cookie)
    await bot.send(ev, f"[CQ:music,type=163,id={song_id}]")
    song_comments = requests.get(
        f'http://127.0.0.1:3000/comment/hot?id={song_id}&type=0&limit={COMMENTS_LIMIT}', cookies=cookie)
    song_comments = song_comments.json()
    try:
        output_comments = "下面为您播送热评：\n"
        for i in range(COMMENTS_LIMIT):
            output_comments = output_comments + \
                song_comments['hotComments'][i]['user']['nickname']+':'
            output_comments = output_comments + \
                song_comments['hotComments'][i]['content']
            if i != COMMENTS_LIMIT-1:
                output_comments = output_comments+'\n'
        await bot.send(ev, output_comments)
    except:
        await bot.send(ev, "这首歌几乎没评论诶……")
    return

@sv.on_fullmatch("查询网易云状态")
async def check_login_status(bot,ev):
    cookie=login()
    await bot.send(ev,check_login_status(cookie=cookie))

def login():
    try:
        f = open(os.path.expanduser('~/.hoshino/cookie.conf'), 'r')
        cookie = eval(f.read())
        print ("已读取保存的cookie")
        return cookie
    except:
        login_url = 'http://127.0.0.1:3000/login/cellphone'
        account_config = {}
        if os.path.exists('./hoshino/modules/songpicker/account.json'):
            with open("./hoshino/modules/songpicker/account.json","r",encoding='utf-8') as dump_f:
                try:
                    # 读取错误一般是人工改动了config并且导致json格式错误
                    account_config = json.load(dump_f)
                    print("已读取网易云账号配置")
                except:
                    account_config = {}
        phone = account_config['phone']
        password = account_config['password']
        login_url = login_url+f'?phone={phone}'+f'&password={password}'
        try:
            res = requests.post(url=login_url)
            cookies = res.cookies
            cookie = requests.utils.dict_from_cookiejar(cookies)
            f = open(os.path.expanduser('~/.hoshino/cookie.conf'), 'w')
            f.write(str(cookie))
            return cookie
        except Exception as err:
            print('获取cookie失败：\n{0}'.format(err))

def get_songid(song_name,cookie):
    search_result = requests.get(
        f'http://127.0.0.1:3000/cloudsearch?keywords={song_name}', cookies=cookie)
    search_result = search_result.json()
    song_id = search_result['result']['songs'][0]['id']
    return song_id

def check_login_status(cookie):
    status_result = requests.get(
        f'http://127.0.0.1:3000/login/status', cookies=cookie)
    status_result=status_result.json()
    if status_result['code'] == 200:
        return f"登录状态正常，用户已登录为：{status_result['profile']['nickname']}"
    else:
        return f"登录状态异常，错误码{status_result['code']}"