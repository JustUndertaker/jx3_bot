import re

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from nonebot.typing import T_State
from src.utils.log import logger

from . import data_source as source
from .config import city_list

export = export()
export.plugin_name = '疫情查询'
export.plugin_command = "XX疫情|疫情 XX"
export.plugin_usage = '查询疫情情况。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件


yiqing = on_regex(r"([\u4e00-\u9fa5]+疫情$)|(^疫情 [\u4e00-\u9fa5]+$)", permission=GROUP,  priority=5, block=True)


@yiqing.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    message_str = event.get_plaintext()
    name = _get_name(message_str)

    province = ""
    city = None

    if name in city_list.keys():
        province = name
    else:
        for key in city_list.keys():
            if name in city_list.get(key):
                province = key
                city = name

    if province:
        msg = await source.get_yiqing_card(province, city)
        name = event.sender.card
        if name == '':
            name = event.sender.nickname
        log = f'{name}（{event.user_id}，{event.group_id}） - 查询疫情：{city}'
        logger.info(log)
    else:
        msg = MessageSegment.text('疫情查询失败，参数可能不正确！')

    await yiqing.finish(msg)


def _get_name(message_str: str) -> str:
    '''
    :说明
        匹配消息中的城市名称

    :参数
        * message_str：原始消息

    :返回
        * str：疫情city
    '''

    # 匹配前面
    args = re.search(r'[\u4e00-\u9fa5]+[疫情]$', message_str)
    if args is not None:
        # 获得字符串
        loc = re.search('疫情', args.string).span()[0]
        args = args.string[0:loc]
        # 去除前缀
        head = re.search(r'(查一下)|(问一下)|(问问)|(想知道)|(查询)|(查查)', args)
        if head is not None:
            loc = head.span()[1]
            args = args[loc:]
        return args
    else:
        # 匹配后面
        loc = re.search('疫情 ', message_str).span()[1]
        return message_str[loc:]
