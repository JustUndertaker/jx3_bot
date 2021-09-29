import time

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.utils.jx3_soket import send_ws_message

from .data_source import (ger_master_server, get_equipquery_name,
                          get_gonglue_name, get_macro_name, get_medicine_name,
                          get_peizhuang_name, get_qixue_name, get_server,
                          get_update_url, get_xinfa)

export = export()
export.plugin_name = '查询功能'
export.plugin_usage = '提供各种剑网三的查询功能。'
export.ignore = False  # 插件管理器忽略此插件


# 日常查询
daily = on_regex(pattern=r"(^日常$)|(^日常 [\u4e00-\u9fa5]+$)", permission=GROUP, priority=5, block=True)

# 装备查询
equipquery_regex = r"(^(装备)|(属性) [(\u4e00-\u9fa5)|(@)]+$)|(^(装备)|(属性) [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)"
equipquery = on_regex(pattern=equipquery_regex, permission=GROUP, priority=5, block=True)

# 开服查询
open_server_regex = r"(^开服$)|(^开服 [\u4e00-\u9fa5]+$)"
open_server_send = on_regex(pattern=open_server_regex, permission=GROUP, priority=5, block=True)

# 金价查询
gold_query = on_regex(pattern=r"(^金价$)|(^金价 [\u4e00-\u9fa5]+$)", permission=GROUP, priority=5, block=True)

# 奇穴查询
extra_point_regex = r"(^奇穴 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+奇穴$)"
extra_point = on_regex(pattern=extra_point_regex, permission=GROUP, priority=5, block=True)

# 小药查询
medicine_regex = r"(^小药 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+小药$)"
medicine = on_regex(pattern=medicine_regex, permission=GROUP, priority=5, block=True)

# 配装查询
equip_group_query_regex = r"(^配装 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+配装$)"
equip_group_query = on_regex(pattern=equip_group_query_regex, permission=GROUP, priority=5, block=True)

# 宏查询
macro_regex = r"(^宏 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+宏$)"
macro = on_regex(pattern=macro_regex, permission=GROUP, priority=5, block=True)

# 奇遇前置查询
adventure_regex = r"^(前置)|(条件) [\u4e00-\u9fa5]+$"
adventurecondition = on_regex(pattern=adventure_regex, permission=GROUP, priority=5, block=True)

# 科举查询
exam = on_regex(pattern=r"^(考试)|(科举) ", permission=GROUP, priority=5, block=True)

# 攻略查询
raiderse = r"(^攻略 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+攻略$)"
raiderse = on_regex(pattern=raiderse, permission=GROUP, priority=5, block=True)

# 挂件查询
pendant = on_regex(pattern=r'^挂件 [\u4e00-\u9fa5]+$', permission=GROUP, priority=5, block=True)


# -----使用jx3pai-----
# 花价查询
flowers_regex = r"(^花价$)|(^花价 [\u4e00-\u9fa5]+$)"
flowers = on_regex(pattern=flowers_regex, permission=GROUP, priority=5, block=True)

# 更新公告
update_regex = r"(^更新$)|(^公告$)|(^更新公告$)"
update_query = on_regex(pattern=update_regex, permission=GROUP, priority=5, block=True)

# 物价查询
price_query = on_regex(pattern=r"^物价 [\u4e00-\u9fa5]+$", permission=GROUP, priority=5, block=True)

# 奇遇查询
serendipity = on_regex(pattern=r"(^奇遇 [(\u4e00-\u9fa5)|(@)]+$)|(^奇遇 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)",
                       permission=GROUP, priority=5, block=True)

# 奇遇列表
serendipityList = on_regex(pattern=r"(^查询 [\u4e00-\u9fa5]+$)|(^查询 [\u4e00-\u9fa5]+ [\u4e00-\u9fa5]+$)",
                           permission=GROUP, priority=5, block=True)


@daily.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''日常查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await ger_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await daily.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    data = {
        "type": 1001,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=data, echo=echo, group_id=group_id, server=server)
    await daily.finish()


@equipquery.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''装备查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    server, name = get_equipquery_name(text)
    if server is None:
        server = await get_server(bot_id, group_id)
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
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await ger_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await daily.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    msg = {
        "type": 1002,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id, server=server)
    await open_server_send.finish()


@gold_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''金价查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await ger_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await daily.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    msg = {
        "type": 1003,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id, server=server)
    await open_server_send.finish()


@extra_point.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇穴查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_qixue_name(text)
    name = get_xinfa(get_name)
    msg = {
        "type": 1008,
        "name": name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@medicine.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''小药查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_medicine_name(text)
    name = get_xinfa(get_name)
    msg = {
        "type": 1010,
        "name": name,
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
    name = get_xinfa(get_name)
    msg = {
        "type": 1011,
        "name": name,
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


@equip_group_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''配装查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_peizhuang_name(text)
    name = get_xinfa(get_name)
    msg = {
        "type": 1006,
        "name": name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@raiderse.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''攻略查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_gonglue_name(text)
    msg = {
        "type": 1023,
        "name": get_name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@flowers.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''花价查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    echo = int(time.time())
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await ger_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await daily.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    msg = {
        "type": 1004,
        "server": server,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id, server=server)
    await open_server_send.finish()


@update_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''更新公告'''
    data = await get_update_url()
    if data['code'] == 200:
        img = data['data']['url']
        msg = MessageSegment.image(img)
    else:
        msg = data['msg']
    await flowers.finish(msg)


@price_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''物价查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    name = text.split(' ')[-1]
    msg = {
        "type": 1012,
        "name": name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id)
    await open_server_send.finish()


@serendipity.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇遇查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        name = text_list[1]
    else:
        text_server = text_list[1]
        name = text_list[2]
        server = await ger_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await serendipity.finish(msg)
    msg = {
        "type": 1018,
        "server": server,
        "name": name,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id, server=server)
    await open_server_send.finish()


@serendipityList.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇遇列表查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        serendipity = text_list[1]
    else:
        text_server = text_list[1]
        serendipity = text_list[2]
        server = await ger_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await serendipity.finish(msg)
    msg = {
        "type": 1018,
        "server": server,
        "serendipity": serendipity,
        "echo": echo
    }
    await send_ws_message(msg=msg, echo=echo, group_id=group_id, server=server)
    await serendipityList.finish()
