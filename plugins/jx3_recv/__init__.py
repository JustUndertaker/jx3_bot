from nonebot.plugin import on
from nonebot.adapters.cqhttp import Bot
from datetime import datetime
from nonebot.plugin import export
from .data_source import get_server
from utils.log import logger
from utils.jx3_event import (
    OpenServerRecvEvent,
    NewsRecvEvent,
    AdventureRecvEvent
)

export = export()
export.plugin_name = '信息推送'
export.plugin_usage = '服务器主动推送消息。'
export.ignore = False  # 插件管理器忽略此插件


open_server_recv = on(type="open_server_recv", priority=5, block=True)  # 开服推送
news_recv = on(type="news_recv", priority=5, block=True)  # 新闻推送
adventure_recv = on(type="adventure_recv", priority=5, block=True)  # 奇遇推送


@open_server_recv.handle()
async def _(bot: Bot, event: OpenServerRecvEvent):
    '''
    开服推送事件
    '''
    server = event.server
    stauts = event.status
    msg = None
    time_now = datetime.now().strftime("%H时%M分")
    if stauts:
        msg = f'时间：{time_now}\n[{server}] 开服啦！'
    group_list = await bot.get_group_list()
    for group in group_list:
        group_server = await get_server(group['group_id'])
        if group_server == server:
            await bot.send_group_msg(group_id=group['group_id'], message=msg)
    log = f'开服推送事件：[{server}]，时间[{time_now}]'
    logger.info(log)
    await open_server_recv.finish()


@news_recv.handle()
async def _(bot: Bot, event: NewsRecvEvent):
    '''
    新闻推送事件
    '''
    news_type = event.news_type
    news_tittle = event.news_tittle
    news_url = event.news_url
    news_date = event.news_date

    msg = f"[{news_type}]来惹\n标题：{news_tittle}\nurl：{news_url}\n日期：{news_date}"
    group_list = await bot.get_group_list()
    for group in group_list:
        await bot.send_group_msg(group_id=group['id'], message=msg)
    log = f'新闻推送事件：[{news_type}]，标题[{news_tittle}]'
    logger.info(log)
    await news_recv.finish()


@adventure_recv.handle()
async def _(bot: Bot, event: AdventureRecvEvent):
    '''
    奇遇推送事件
    '''
    server = event.server
    msg = f'奇遇播报 {event.time}\n{event.serendipity} 被 {event.name} 抱走惹。'
    log = f'奇遇推送事件：{msg}'
    logger.debug(log)
    group_list = await bot.get_group_list()
    for group in group_list:
        group_server = await get_server(group['group_id'])
        if group_server == server:
            await bot.send_group_msg(group_id=group['group_id'], message=msg)
    await adventure_recv.finish()
