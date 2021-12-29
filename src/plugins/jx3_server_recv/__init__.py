import asyncio
import random
from datetime import datetime

from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export, on
from src.utils.jx3_event import OpenServerRecvEvent
from src.utils.utils import GroupList_Async

from . import data_source as source

export = export()
export.plugin_name = '开服推送'
export.plugin_command = "无"
export.plugin_usage = '推送开服信息。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件


open_server_recv = on(type="open_server_recv", priority=5, block=True)  # 开服推送


@open_server_recv.handle()
async def _(bot: Bot, event: OpenServerRecvEvent):
    '''
    开服推送事件
    '''
    bot_id = int(bot.self_id)
    server = event.server
    stauts = event.status
    msg = None
    time_now = datetime.now().strftime("%H时%M分")
    if stauts:
        msg = f'时间：{time_now}\n[{server}] 开服啦！'
    else:
        msg = f'时间{time_now}\n[{server}]维护惹。'
    group_list = await bot.get_group_list()
    async for group_id in GroupList_Async(group_list):
        group_server = await source.get_server(bot_id, group_id)
        if group_server == server:
            # 判断机器人是否开启
            status = await source.get_robot_status(bot_id, group_id)
            if status:
                try:
                    await bot.send_group_msg(group_id=group_id, message=msg)
                    await asyncio.sleep(random.uniform(0.3, 0.5))
                except Exception:
                    pass
    await open_server_recv.finish()
