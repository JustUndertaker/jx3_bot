from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from .data_source import get_server
from nonebot.plugin import export
from nonebot import on_regex
import time
from utils.jx3_soket import send_ws_message


export = export()
export.plugin_name = '查询功能'
export.plugin_usage = '提供各种剑网三的查询功能。'
export.ignore = False  # 插件管理器忽略此插件


daily = on_regex(pattern=r'^日常$', permission=GROUP, priority=5, block=True)  # 日常查询
equipquery = on_regex(pattern=r'^装备 [\u4e00-\u9fa5]+$', permission=GROUP, priority=5, block=True)  # 装备查询


@daily.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    echo = int(time.time())
    group_id = event.group_id
    server = await get_server(group_id)
    data = {
        "type": 1001,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=data, echo=echo, group_id=group_id)
    await daily.finish()


@equipquery.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    echo = int(time.time())
    group_id = event.group_id
    server = await get_server(group_id)
    name = event.get_plaintext().split(" ")[-1]
    msg = {
        "type": 1025,
        "server": server,
        "name": name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await equipquery.finish()
