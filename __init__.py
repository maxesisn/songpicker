from hoshino import Service
import requests

sv = Service("点歌")


@sv.on_prefix("点歌")
async def pick_song(bot, ev):
    song_name = ev.message.extract_plain_text()
    if not song_name:
        await bot.send(ev,"要加上歌曲名才能点歌！")
        return
    search_result=requests.get('')