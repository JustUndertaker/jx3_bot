import re

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from nonebot.typing import T_State
from src.utils.log import logger

from .config import city_list
from .data_source import get_yiqing_card

export = export()
export.plugin_name = '疫情查询'
export.plugin_usage = '查询疫情情况。'
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
        msg = await get_yiqing_card(province, city)
        name = event.sender.card
        if name == '':
            name = event.sender.nickname
        log = f'{name}（{event.user_id}，{event.group_id}） - 查询疫情：{city}'
        logger.info(log)
    else:
        msg = MessageSegment.text('参数不对，不对！')

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
