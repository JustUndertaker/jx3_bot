from datetime import datetime

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.utils.browser import get_html_screenshots, get_web_screenshot
from src.utils.log import logger

from .data_source import (get_daily_week, get_data_from_jx3api,
                          get_equipquery_name, get_gonglue_name, get_jx3sp_img,
                          get_macro_name, get_master_server, get_medicine_name,
                          get_peizhuang_name, get_qixue_name, get_server,
                          get_xinfa, hand_adventure_data, handle_data,
                          indicator_query_hanlde)

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
indicator_regex = r"(^战绩 [(\u4e00-\u9fa5)|(@)]+$)|(^战绩 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)"
indicator = on_regex(pattern=indicator_regex, permission=GROUP, priority=5, block=True)

# 名剑排行查询
awesome_query_regex = r"(^名剑排行 [0-9]+$)|(^名剑排行$)"
awesome_query = on_regex(pattern=awesome_query_regex, permission=GROUP, priority=5, block=True)

# 团本记录查询
teamcdlist_regex = r"(^副本记录 [(\u4e00-\u9fa5)|(@)]+$)|(^副本记录 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)"
teamcdlist = on_regex(pattern=teamcdlist_regex, permission=GROUP, priority=5, block=True)


# 沙盘查询
sand_query_regex = r"(^沙盘$)|(^沙盘 [\u4e00-\u9fa5]+$)"
sand_query = on_regex(pattern=sand_query_regex, permission=GROUP, priority=5, block=True)


@daily.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''日常查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await get_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await daily.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询日常：server：{server}"
    logger.info(log)

    app = "daily"
    params = {
        "server": server,
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await daily.finish(msg)

    msg = f'日常[{server}]\n'
    msg += f'当前时间：{data.get("DateTime")} 星期{data.get("Week")}\n'
    msg += f'今日大战：{data.get("DayWar")}\n'
    msg += f'今日战场：{data.get("DayBattle")}\n'
    msg += f'公共任务：{data.get("DayCommon")}\n'
    msg += f'阵营任务：{data.get("DayCamp")}\n'
    msg += get_daily_week(data.get("Week"))
    if data.get("DayDraw") is not None:
        msg += f'美人画像：{data.get("DayDraw")}\n'
    msg += f'\n武林通鉴·公共任务\n{data.get("WeekCommon")}\n'
    msg += f'武林通鉴·秘境任务\n{data.get("WeekFive")}\n'
    msg += f'武林通鉴·团队秘境\n{data.get("WeekTeam")}'
    await daily.finish(msg)


@equipquery.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''装备查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    server, name = get_equipquery_name(text)
    if server is None:
        server = await get_server(bot_id, group_id)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询装备：server：{server}，name：{name}"
    logger.info(log)

    app_type = 'roles'
    app = 'attribute'
    params = {
        "server": server,
        "name": name
    }
    req_msg, req_data = await get_data_from_jx3api(app=app, params=params, app_type=app_type)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await equipquery.finish(msg)

    data = await handle_data(req_data)
    pagename = "equip.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await equipquery.finish(msg)


@open_server_send.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''开服查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await get_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await open_server_send.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询开服：server：{server}"
    logger.info(log)

    app = 'check'
    params = {
        "server": server
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await open_server_send.finish(msg)

    status = "已开服" if data['status'] == 1 else "维护中"
    msg = f'{data.get("server")} 当前状态是[{status}]'
    await open_server_send.finish(msg)


@gold_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''金价查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await get_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await gold_query.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询金价：server：{server}"
    logger.info(log)

    app = 'demon'
    params = {
        "server": server
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await gold_query.finish(msg)

    date_now = datetime.now().strftime("%m-%d %H:%M")
    msg = f'金价[{data.get("server")}] {date_now}\n'
    msg += f'官方平台：1元={data.get("wanbaolou")}金\n'
    msg += f'悠悠平台：1元={data.get("uu898")}金\n'
    msg += f'嘟嘟平台：1元={data.get("dd373")}金\n'
    msg += f'其他平台：1元={data.get("5173")}金'
    await gold_query.finish(msg)


@extra_point.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇穴查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_qixue_name(text)
    name = get_xinfa(get_name)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询奇穴：name：{name}"
    logger.info(log)

    app = 'qixue'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await extra_point.finish(msg)

    msg = f'[{data.get("name")}]\n'
    msg += f'龙门绝境奇穴：\n{data.get("long")}\n'
    msg += f'战场任务奇穴：\n{data.get("battle")}\n'
    await extra_point.finish(msg)


@medicine.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''小药查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_medicine_name(text)
    name = get_xinfa(get_name)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询小药：name：{name}"
    logger.info(log)

    app = 'heighten'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await medicine.finish(msg)

    msg = f'[{data.get("name")}]小药：\n'
    msg += f'增强食品：{data.get("heightenFood")}\n'
    msg += f'辅助食品：{data.get("auxiliaryFood")}\n'
    msg += f'增强药品：{data.get("heightenDrug")}\n'
    msg += f'辅助药品：{data.get("auxiliaryDrug")}'

    await medicine.finish(msg)


@macro.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''宏查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_macro_name(text)
    name = get_xinfa(get_name)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询宏：name：{name}"
    logger.info(log)

    app = 'macro'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await macro.finish(msg)

    msg = f'宏 {data.get("name")} 更新时间：{data.get("time")}\n'
    msg += f'{data.get("command")}\n'
    msg += f'奇穴：{data.get("holes")}'

    await macro.finish(msg)


@adventurecondition.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''前置查询'''
    group_id = event.group_id
    name = event.get_plaintext().split(" ")[-1]
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询前置：name：{name}"
    logger.info(log)

    app = 'require'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await adventurecondition.finish(msg)

    url = data.get("url")
    msg = MessageSegment.image(url)
    await adventurecondition.finish(msg)


@exam.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''科举查询'''
    group_id = event.group_id
    question = event.get_plaintext()[3:]
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询科举：question：{question}"
    logger.info(log)

    app = 'exam'
    params = {
        "question":  question
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await exam.finish(msg)
    data: list = data[0]
    msg = f'[问题]\n{data.get("question")}\n'
    msg += f'[答案]\n{data.get("answer")}'
    await exam.finish(msg)


@equip_group_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''配装查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    get_name = get_peizhuang_name(text)
    name = get_xinfa(get_name)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询配装：name：{name}"
    logger.info(log)

    app = 'equip'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await equip_group_query.finish(msg)

    msg = MessageSegment.text(f'{data.get("name")}配装：\nPve装备：\n')+MessageSegment.image(data.get("pveUrl")) + \
        MessageSegment.text("Pvp装备：\n")+MessageSegment.image(data.get("pvpUrl"))
    await equip_group_query.finish(msg)


@raiderse.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''攻略查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    name = get_gonglue_name(text)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询攻略：name：{name}"
    logger.info(log)

    app = 'strategy'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await raiderse.finish(msg)

    img = data.get("url")
    msg = MessageSegment.image(img)
    await raiderse.finish(msg)


@flowers.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''花价查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await get_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await flowers.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询花价：server：{server}"
    logger.info(log)

    app = 'flower'
    params = {
        "server": server
    }
    req_msg, req_data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await flowers.finish(msg)

    data = {}
    data["server"] = server
    data["data"] = req_data
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['time'] = now_time
    pagename = "flower.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await flowers.finish(msg)


@update_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''更新公告'''
    url = "https://jx3.xoyo.com/launcher/update/latest.html"
    img = await get_web_screenshot(url=url, width=130)
    msg = MessageSegment.image(img)
    log = f"Bot({bot.self_id}) | 群[{event.group_id}]查询更新公告"
    logger.info(log)
    await update_query.finish(msg)


@price_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''物价查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    name = text.split(' ')[-1]
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询物价：name：{name}"
    logger.info(log)

    app = 'price'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await price_query.finish(msg)

    pagename = "itemprice.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await price_query.finish(msg)


@serendipity.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇遇查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        name = text_list[1]
    else:
        text_server = text_list[1]
        name = text_list[2]
        server = await get_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await serendipity.finish(msg)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询奇遇：server：{server}，name：{name}"
    logger.info(log)

    app = 'serendipity'
    params = {
        "server": server,
        "name": name
    }
    req_msg, req_data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await serendipity.finish(msg)

    data = {}
    data["server"] = server
    data["data"] = hand_adventure_data(req_data)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['time'] = now_time
    pagename = "adventure.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await serendipity.finish(msg)


@serendipityList.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''奇遇列表查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        serendipity = text_list[1]
    else:
        text_server = text_list[1]
        serendipity = text_list[2]
        server = await get_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await serendipityList.finish(msg)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询奇遇列表：server：{server}，serendipity：{serendipity}"
    logger.info(log)

    app = 'recent'
    params = {
        "server": server,
        "serendipity": serendipity
    }
    req_msg, req_data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await serendipityList.finish(msg)

    data = {}
    data["server"] = server
    data["data"] = hand_adventure_data(req_data)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['time'] = now_time
    pagename = "adventure.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await serendipityList.finish(msg)


@saohua_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''骚话'''
    group_id = event.group_id
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询请求骚话"
    logger.info(log)

    app = 'random'
    params = {}
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await saohua_query.finish(msg)

    msg = data.get('text')
    await saohua_query.finish(msg)


@furniture_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''装饰查询'''
    group_id = event.group_id
    text = event.get_plaintext()
    name = text.split(' ')[-1]
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询装饰：name：{name}"
    logger.info(log)

    app = 'furniture'
    params = {
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await furniture_query.finish(msg)

    pagename = "furniture.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await furniture_query.finish(msg)


@seniority_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''资历排行查询'''
    bot_id = int(bot.self_id)
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
            server = await get_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await seniority_query.finish(msg)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询资历排行：server：{server}，sect：{sect}"
    logger.info(log)

    app = 'seniority'
    params = {
        "server": server,
        "sect": sect
    }
    req_msg, req_data = await get_data_from_jx3api(app=app, params=params)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await seniority_query.finish(msg)

    data = []
    for i in range(10):
        data.append(req_data[i])
    pagename = "seniority.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await seniority_query.finish(msg)


@indicator.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''战绩总览查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        name = text_list[1]
    else:
        text_server = text_list[1]
        name = text_list[2]
        server = await get_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await indicator.finish(msg)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询战绩总览：server：{server}，name：{name}"
    logger.info(log)

    app_type = 'arena'
    app = 'indicator'
    params = {
        "server": server,
        "name": name
    }
    req_msg, req_data = await get_data_from_jx3api(app=app, params=params, app_type=app_type)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await indicator.finish(msg)

    data = {}
    role_info = req_data.get("role_info")
    data['name'] = role_info['server']+"-"+role_info['name']
    data['role_performance'] = req_data.get('role_performance')
    data['history'] = indicator_query_hanlde(req_data.get('role_history'))
    pagename = "indicator.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await indicator.finish(msg)


@awesome_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''名剑排行查询'''
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
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询名剑排名：match：{params}"
    logger.info(log)

    app_type = 'arena'
    app = 'awesome'
    params = {
        "match": match,
        "limit": 10
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params, app_type=app_type)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await awesome_query.finish(msg)

    pagename = "awesome_query.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await awesome_query.finish(msg)


@teamcdlist.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''副本记录查询'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    text_list = text.split(' ')
    if len(text_list) == 2:
        server = await get_server(bot_id, group_id)
        name = text_list[1]
    else:
        text_server = text_list[1]
        name = text_list[2]
        server = await get_master_server(text_server)
        if server is None:
            msg = "查询出错，请输入正确的服务器名."
            await teamcdlist.finish(msg)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询副本记录：server：{server}，name：{name}"
    logger.info(log)

    app_type = 'roles'
    app = 'teamcdlist'
    params = {
        "server": server,
        "name": name
    }
    req_msg, data = await get_data_from_jx3api(app=app, params=params, app_type=app_type)
    if req_msg != 'success':
        msg = f"查询失败，{req_msg}。"
        await teamcdlist.finish(msg)

    pagename = "teamcdlist.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await teamcdlist.finish(msg)


@sand_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    沙盘查询
    '''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext().split(" ")
    if len(text) > 1:
        server_text = text[-1]
        server = await get_master_server(server_text)
        if server is None:
            msg = "查询错误，请输入正确的服务器名。"
            await flowers.finish(msg)
    else:
        server = await get_server(bot_id, group_id)
    log = f"Bot({bot.self_id}) | 群[{group_id}]查询沙盘：server：{server}"
    logger.info(log)

    flag, data = await get_jx3sp_img(server)
    if flag:
        text = f"[{server}]沙盘 更新时间 {data.get('createTime')}"
        img = data.get('sandImage')
        msg = MessageSegment.text(text)+MessageSegment.image(img)
    else:
        msg = f"查询失败，{data}"

    await raiderse.finish(msg)
