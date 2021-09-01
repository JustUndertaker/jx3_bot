from nonebot import get_driver
from utils.jx3_event import OpenServerEvent, NewsEvent, AdventureEvent
from utils.jx3_soket import on_connect
from nonebot.plugin import on
from nonebot.adapters.cqhttp import Bot
import asyncio

from nonebot.plugin import export

export = export()
export.plugin_name = '剑三api'
export.plugin_usage = '剑网三的api'

driver = get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    loop = asyncio.get_event_loop()
    loop.create_task(on_connect(loop, bot))


# 注册handler
openserver = on(type="OpenServer", priority=5, block=True)


@openserver.handle()
async def _(bot: Bot, event: OpenServerEvent):
    server = event.data['server']
    stauts = event.data['stauts']
    msg = None
    if stauts == 1:
        msg = f'[{server}] 开服啦！'
    group_list = await bot.get_group_list()
    for group in group_list:
        await bot.send_group_msg(group_id=group['id'], message=msg)
    await openserver.finish()


news = on(type="news", priority=5, block=True)


@news.handle()
async def _(bot: Bot, event: NewsEvent):
    news_type = event.data['type']
    news_tittle = event.data['title']
    news_url = event.data['url']
    news_date = event.data['date']

    msg = f"[{news_type}]\n{news_tittle}\nurl：{news_url}\n日期：{news_date}"
    group_list = await bot.get_group_list()
    for group in group_list:
        await bot.send_group_msg(group_id=group['id'], message=msg)
    await news.finish()


adventure = on(type="adventure", priority=5, block=True)


@adventure.handle()
async def _(bot: Bot, event: AdventureEvent):
    server = event.data['server']
    name = event.data['name']
    time_now = event.data['time']
    #timeArray = time.localtime(time)
    #time_now = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    serendipity = event.data['serendipity']
    msg = f'[{server}] 的 [{name}] 出奇遇了。\n奇遇：{serendipity}\n时间：{time_now}'
    group_list = await bot.get_group_list()
    for group in group_list:
        await bot.send_group_msg(group_id=group['group_id'], message=msg)
    await adventure.finish()
