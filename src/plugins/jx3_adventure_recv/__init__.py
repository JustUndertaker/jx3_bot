from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export, on
from src.utils.jx3_event import AdventureRecvEvent
from src.utils.log import logger

from .data_source import get_robot_status, get_server

export = export()
export.plugin_name = '奇遇推送'
export.plugin_usage = '推送奇遇消息。'
export.ignore = False  # 插件管理器忽略此插件


adventure_recv = on(type="adventure_recv", priority=5, block=True)  # 奇遇推送


@adventure_recv.handle()
async def _(bot: Bot, event: AdventureRecvEvent):
    '''
    奇遇推送事件
    '''
    bot_id = int(bot.self_id)
    server = event.server
    msg = f'奇遇播报 {event.time}\n{event.serendipity} 被 {event.name} 抱走惹。'
    log = f'奇遇推送事件：[{server}]{event.serendipity} 触发者：{event.name} '
    logger.debug(log)
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group['group_id']
        group_server = await get_server(bot_id, group_id)
        if group_server == server:
            # 判断机器人开关
            status = await get_robot_status(bot_id, group_id)
            if status:
                await bot.send_group_msg(group_id=group_id, message=msg)
    await adventure_recv.finish()
