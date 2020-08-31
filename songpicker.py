from hoshino import Service
import requests

sv = Service("点歌")


@sv.on_prefix("点歌")
async def pick_song(bot, ev):
    song_name = ev.message.extract_plain_text()
    if not song_name:
        await bot.send(ev, "要加上歌曲名才能点歌！")
        return
    search_result = requests.get(
        f'http://127.0.0.1:3000/search?keywords={song_name}')
    search_result=search_result.json()
    song_id = search_result['result']['songs'][0]['id']
    await bot.send(ev, f"[CQ:music,type=163,id={song_id}]")
