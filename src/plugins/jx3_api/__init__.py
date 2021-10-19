from nonebot.adapters.cqhttp import Bot, MessageSegment
from nonebot.plugin import export, on
from src.server.jx3_event import (AwesomeQueryEvent, EquipQueryEvent,
                                  IndicatorQueryEvent, TeamCdListEvent)
from src.utils.browser import get_html_screenshots

from .data_source import handle_data, indicator_query_hanlde

export = export()
export.plugin_name = 'ws链接回复'
export.plugin_command = ""
export.plugin_usage = '用于jx3_api的ws链接，处理服务器主动发送后回复的信息。'
export.ignore = True  # 插件管理器忽略此插件


equip_query = on(type="equipquery", priority=6, block=True)  # 角色装备查询
indicator_query = on(type="indicator", priority=6, block=True)  # 战绩查询
awesome_query = on(type="awesomequery", priority=6, block=True)  # 名剑排行查询
teamcdlist_query = on(type="teamcdlist", priority=6, block=True)  # 团本记录查询


@equip_query.handle()
async def _(bot: Bot, event: EquipQueryEvent):
    '''
    角色装备查询
    '''
    if event.msg_success != "success":
        msg = f'查询失败，{event.msg_success}。'
        await equip_query.finish(msg)
    get_data = event.data

    # 数据预处理
    data = await handle_data(get_data)
    pagename = "equip.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await equip_query.finish(msg)


@indicator_query.handle()
async def _(bot: Bot, event: IndicatorQueryEvent):
    '''战绩查询'''
    if event.msg_success != "success":
        msg = f'查询失败，{event.msg_success}。'
        await indicator_query.finish(msg)
    data = {}
    role_info = event.role_info
    data['name'] = role_info['server']+"-"+role_info['name']
    data['role_performance'] = event.role_performance
    data['history'] = indicator_query_hanlde(event.role_history)
    pagename = "indicator.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await indicator_query.finish(msg)


@awesome_query.handle()
async def _(bot: Bot, event: AwesomeQueryEvent):
    '''名剑排行查询'''
    if event.msg_success != "success":
        msg = f'查询失败，{event.msg_success}。'
        await awesome_query.finish(msg)
    data = event.data
    pagename = "awesome_query.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await equip_query.finish(msg)


@teamcdlist_query.handle()
async def _(bot: Bot, event: TeamCdListEvent):
    '''团本记录查询'''
    if event.msg_success != "success":
        msg = f'查询失败，{event.msg_success}。'
        await teamcdlist_query.finish(msg)
    data = event.data
    pagename = "teamcdlist.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    await teamcdlist_query.finish(msg)
