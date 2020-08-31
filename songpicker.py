import os
from requests import cookies
from hoshino import Service
import requests
import json

sv = Service("点歌")


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
        f'http://127.0.0.1:3000/comment/hot?id={song_id}&type=0&limit=3', cookies=cookie)
    song_comments = song_comments.json()
    try:
        output_comments = "下面为您播送热评：\n"
        for i in range(3):
            output_comments = output_comments + \
                song_comments['hotComments'][i]['user']['nickname']+':'
            output_comments = output_comments + \
                song_comments['hotComments'][i]['content']
            if i != 2:
                output_comments = output_comments+'\n'
        await bot.send(ev, output_comments)
    except:
        await bot.send(ev, "这首歌几乎没评论诶……")
    return


def login():
    try:
        f = open(os.path.expanduser('~/.hoshino/cookie.conf'), 'r')
        cookie = eval(f.read())
        print ("已读取保存的cookie")
        return cookie
    except:
        login_url = 'http://127.0.0.1:3000/login/cellphone'
        phone = '14729020242'
        password = 'snwbc710286'
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
    