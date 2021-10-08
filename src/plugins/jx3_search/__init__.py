import time

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.server.jx3_soket import send_ws_message
from src.utils.browser import get_web_screenshot
from src.utils.log import logger

from .data_source import (ger_master_server, get_equipquery_name,
                          get_gonglue_name, get_macro_name, get_medicine_name,
                          get_peizhuang_name, get_qixue_name, get_server,
                          get_xinfa)

export = export()
export.plugin_name = '查询功能'
export.plugin_command = "参考“帮助”"
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

# 骚话
saohua_query = on_regex(pattern=r"^骚话$", permission=GROUP, priority=5, block=True)

# 装饰查询
furniture_query = on_regex(pattern=r"^装饰 [\u4e00-\u9fa5]+$", permission=GROUP, priority=5, block=True)

# 资历查询
seniority_regex = r"(^资历排行 [\u4e00-\u9fa5]+$)|(^资历排行 [\u4e00-\u9fa5]+ [\u4e00-\u9fa5]+$)"
seniority_query = on_regex(pattern=seniority_regex, permission=GROUP, priority=5, block=True)

# 战绩总览查询
indicator_overview_regex = r"(^战绩 [(\u4e00-\u9fa5)|(@)]+$)|(^战绩 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)"
indicator_overview = on_regex(pattern=indicator_overview_regex, permission=GROUP, priority=5, block=True)

# 历史战绩查询
indicator_history_regex = r"(^历史战绩 [(\u4e00-\u9fa5)|(@)]+$)|(^历史战绩 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)"
indicator_history = on_regex(pattern=indicator_history_regex, permission=GROUP, priority=5, block=True)

# 名剑排行查询
awesome_query_regex = r"(^名剑排行 [0-9]+$)|(^名剑排行$)"
awesome_query = on_regex(pattern=awesome_query_regex, permission=GROUP, priority=5, block=True)

# 团本记录查询
teamcdlist_regex = r"(^副本记录 [(\u4e00-\u9fa5)|(@)]+$)|(^副本记录 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)"
teamcdlist = on_regex(pattern=teamcdlist_regex, permission=GROUP, priority=5, block=True)


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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询日常：server：{server}"
    logger.info(log)
    await send_ws_message(msg=data, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询装备：server：{server}，name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询开服：server：{server}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询金价：server：{server}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询奇穴：name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询小药：name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询宏：name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询前置：name：{get_name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询科举：question：{question}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询挂件：name：{get_name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询配装：name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询攻略：name：{get_name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询花价：server：{server}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
    await open_server_send.finish()


@update_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''更新公告'''
    url = "https://jx3.xoyo.com/launcher/update/latest.html"
    img = await get_web_screenshot(url=url, width=130)
    msg = MessageSegment.image(img)
    log = f"Bot({bot.self_id}) | 群[{event.group_id}]查询更新公告"
    logger.info(log)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询物价：name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询奇遇：server：{server}，name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询奇遇列表：server：{server}，serendipity：{serendipity}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
    await serendipityList.finish()


@saohua_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''骚话'''
    echo = int(time.time())
    group_id = event.group_id
    msg = {
        "type": 1019,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询请求骚话"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
    await saohua_query.finish()


@furniture_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''装饰查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    name = text.split(' ')[-1]
    msg = {
        "type": 1016,
        "name": name,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询装饰：name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
    await furniture_query.finish()


@seniority_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''资历排行查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        sect = text_list[1]
    else:
        text_server = text_list[1]
        sect = text_list[2]
        if sect == "全门派" or sect == "全职业":
            sect = "all"
        if text_server == "全区服":
            server = "全区服"
        else:
            server = await ger_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await seniority_query.finish(msg)
    msg = {
        "type": 1022,
        "server": server,
        "sect": sect,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询资历排行：server：{server}，sect：{sect}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
    await seniority_query.finish()


@indicator_overview.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''战绩总览查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    params = "overview"
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
            await indicator_overview.finish(msg)
    msg = {
        "type": 1026,
        "server": server,
        "name": name,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询战绩总览：server：{server}，name：{name}"
    logger.info(log)

    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server, params=params)
    await indicator_overview.finish()


@indicator_history.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''战绩总览查询'''
    bot_id = int(bot.self_id)
    echo = int(time.time())
    group_id = event.group_id
    params = "history"
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
            await indicator_history.finish(msg)
    msg = {
        "type": 1026,
        "server": server,
        "name": name,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询战绩总览：server：{server}，name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server, params=params)
    await indicator_history.finish()


@awesome_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''名剑排行查询'''
    echo = int(time.time())
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 1:
        match = 22
    else:
        _match = text_list[1]
        if _match == "22":
            match = 22
        elif _match == "33":
            match = 33
        elif _match == "55":
            match = 55
        else:
            msg = "查询出错，请输入正确的参数。"
            await awesome_query.finish(msg)
    params = str(match)
    msg = {
        "type": 1027,
        "match": match,
        "limit": 10,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询名剑排名：match：{params}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id)
    await awesome_query.finish()


@teamcdlist.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''副本记录查询'''
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
            await teamcdlist.finish(msg)
    msg = {
        "type": 1029,
        "server": server,
        "name": name,
        "echo": echo
    }
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询副本记录：server：{server}，name：{name}"
    logger.info(log)
    await send_ws_message(msg=msg, echo=echo, bot_id=bot.self_id, group_id=group_id, server=server)
    await teamcdlist.finish()
