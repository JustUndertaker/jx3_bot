from datetime import datetime

from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export, on
from src.utils.jx3_event import OpenServerRecvEvent
from src.utils.log import logger

from .data_source import get_robot_status, get_server

export = export()
export.plugin_name = '开服推送'
export.plugin_usage = '推送开服信息。'
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
    for group in group_list:
        group_id = group['group_id']
        group_server = await get_server(bot_id, group_id)
        if group_server == server:
            # 判断机器人是否开启
            status = await get_robot_status(bot_id, group_id)
            if status:
                await bot.send_group_msg(group_id=group_id, message=msg)
    log = f'开服推送事件：[{server}]，时间[{time_now}]'
    logger.info(log)
    await open_server_recv.finish()
