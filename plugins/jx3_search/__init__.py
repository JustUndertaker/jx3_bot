from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from .data_source import get_server, get_macro_name
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
open_server_send = on_regex(pattern=r'^开服$', permission=GROUP, priority=5, block=True)  # 开服查询
gold_query = on_regex(pattern=r'^金价$', permission=GROUP, priority=5, block=True)  # 金价查询
extra_point = on_regex(pattern=r'^奇穴 [\u4e00-\u9fa5]+$', permission=GROUP, priority=5, block=True)  # 奇穴查询
medicine = on_regex(pattern=r'^小药 [\u4e00-\u9fa5]+$', permission=GROUP, priority=5, block=True)  # 小药查询

macro_regex = r"(^宏 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+宏$)"
macro = on_regex(pattern=macro_regex, permission=GROUP, priority=5, block=True)  # 宏查询

adventure_regex = r"^(前置)|(条件) [\u4e00-\u9fa5]+$"
adventurecondition = on_regex(pattern=adventure_regex, permission=GROUP, priority=5, block=True)  # 奇遇前置查询

exam = on_regex(pattern=r"^(考试)|(科举) ", permission=GROUP, priority=5, block=True)  # 科举查询
pendant = on_regex(pattern=r'^挂件 [\u4e00-\u9fa5]+$', permission=GROUP, priority=5, block=True)  # 挂件查询
# raiderse_search = pendant = on_regex(pattern=r'^奇遇 [\u4e00-\u9fa5]+$', permission=GROUP, priority=5, block=True)  # 奇遇查询


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


@open_server_send.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''开服查询'''
    echo = int(time.time())
    group_id = event.group_id
    server = await get_server(group_id)
    msg = {
        "type": 1002,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@gold_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''金价查询'''
    echo = int(time.time())
    group_id = event.group_id
    server = await get_server(group_id)
    msg = {
        "type": 1003,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@extra_point.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇穴查询'''
    echo = int(time.time())
    group_id = event.group_id
    get_name = event.get_plaintext().split(" ")[-1]
    msg = {
        "type": 1008,
        "name": get_name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@medicine.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''小药查询'''
    echo = int(time.time())
    group_id = event.group_id
    get_name = event.get_plaintext().split(" ")[-1]
    msg = {
        "type": 1010,
        "name": get_name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@macro.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''宏查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_macro_name(text)
    msg = {
        "type": 1011,
        "name": get_name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@adventurecondition.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''前置查询'''
    echo = int(time.time())
    group_id = event.group_id
    get_name = event.get_plaintext().split(" ")[-1]
    msg = {
        "type": 1013,
        "name": get_name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@exam.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''科举查询'''
    echo = int(time.time())
    group_id = event.group_id
    question = event.get_plaintext()[3:]
    msg = {
        "type": 1014,
        "question": question,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@pendant.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''挂件查询'''
    echo = int(time.time())
    group_id = event.group_id
    get_name = event.get_plaintext().split(" ")[-1]
    msg = {
        "type": 1021,
        "name": get_name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()
