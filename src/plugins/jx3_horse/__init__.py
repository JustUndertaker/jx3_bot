import asyncio
import random

from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export, on
from src.utils.jx3_event import HorseCatchedEvent, HorseRefreshEvent
from src.utils.utils import GroupList_Async

from . import data_source as source

export = export()
export.plugin_name = '抓马监控'
export.plugin_command = "-"
export.plugin_usage = '监控抓马，目前只支持部分区服。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件


hores_refresh = on(type="hores_refresh", priority=5, block=True)  # 马驹刷新
hores_catched = on(type="hores_catched", priority=5, block=True)  # 马驹被抓


@hores_refresh.handle()
async def _(bot: Bot, event: HorseRefreshEvent):
    '''
    马驹刷新事件
    '''
    bot_id = int(bot.self_id)
    server = event.server
    map = event.map
    mins = f"{str(event.min)} - {str(event.max)}分"
    get_time = event.time
    msg = f"[抓马监控] 时间：{get_time}\n{map} 将在[{mins}]后刷新马驹。"

    group_list = await bot.get_group_list()
    async for group_id in GroupList_Async(group_list):
        group_server = await source.get_server(bot_id, group_id)
        status = await source.get_robot_status(bot_id, group_id)
        if group_server == server and status:
            try:
                await bot.send_group_msg(group_id=group_id, message=msg)
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await hores_refresh.finish()


@hores_catched.handle()
async def _(bot: Bot, event: HorseCatchedEvent):
    '''
    马驹被抓事件
    '''
    bot_id = int(bot.self_id)
    server = event.server
    name = event.name
    map = event.map
    horse = event.horse
    get_time = event.time
    msg = f"[抓马监控] 时间：{get_time}\n{map} 的 {horse} 被 {name} 抓走了~"

    group_list = await bot.get_group_list()
    async for group_id in GroupList_Async(group_list):
        group_server = await source.get_server(bot_id, group_id)
        status = await source.get_robot_status(bot_id, group_id)
        if group_server == server and status:
            try:
                await bot.send_group_msg(group_id=group_id, message=msg)
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await hores_catched.finish()
