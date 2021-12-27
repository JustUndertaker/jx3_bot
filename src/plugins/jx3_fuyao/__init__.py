import asyncio
import random

from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export, on
from src.utils.jx3_event import FuyaoCatchedEvent, FuyaoRefreshEvent

from . import data_source as source

export = export()
export.plugin_name = '扶摇监控'
export.plugin_command = "-"
export.plugin_usage = '监控扶摇，目前只支持部分区服。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件


fuyao_refresh = on(type="fuyao_refresh", priority=5, block=True)  # 扶摇刷新
fuyao_catched = on(type="fuyao_catched", priority=5, block=True)  # 扶摇点名


@fuyao_refresh.handle()
async def _(bot: Bot, event: FuyaoRefreshEvent):
    '''
    扶摇刷新事件
    '''
    bot_id = int(bot.self_id)
    server = event.server
    get_time = event.time
    msg = f"[扶摇监控]\n扶摇九天在 {get_time} 开启了。"

    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group['group_id']
        group_server = await source.get_server(bot_id, group_id)
        status = await source.get_robot_status(bot_id, group_id)
        if group_server == server and status:
            try:
                await bot.send_group_msg(group_id=group_id, message=msg)
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await fuyao_refresh.finish()


@fuyao_catched.handle()
async def _(bot: Bot, event: FuyaoCatchedEvent):
    '''
    扶摇点名事件
    '''
    bot_id = int(bot.self_id)
    server = event.server
    get_time = event.time
    name = ",".join(event.names)
    msg = f"[扶摇监控] 时间：{get_time}\n唐文羽点名了[{name}]。"

    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group['group_id']
        group_server = await source.get_server(bot_id, group_id)
        status = await source.get_robot_status(bot_id, group_id)
        if group_server == server and status:
            try:
                await bot.send_group_msg(group_id=group_id, message=msg)
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await fuyao_catched.finish()
