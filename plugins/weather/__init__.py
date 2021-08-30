from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot import on_regex
from nonebot.adapters.cqhttp.permission import GROUP
import re
from nonebot.typing import T_State
from utils.log import logger
from .data_source import get_weather_of_city
from nonebot.plugin import export

export = export()
export.plugin_name = '天气'
export.plugin_usage = '普普通通的查天气吧\n命令：XX天气\n天气 XX'

weather = on_regex(r"([\u4e00-\u9fa5]+[天气]$)|(^天气 [\u4e00-\u9fa5]+$)", permission=GROUP, priority=5, block=True)


@weather.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    message_str = event.get_plaintext()
    city = _get_city(message_str)

    # 特殊判定
    if city == '火星':
        msg = MessageSegment.text('没想到你个小呆子还真的想看火星天气！\n火星大气中含有95％的二氧化碳,气压低，加之极度的干燥，'
                                  '就阻止了水的形成积聚。这意味着火星几乎没有云,冰层覆盖了火星的两极，它们的融化和冻结受到火星与太'
                                  '阳远近距离的影响,它产生了强大的尘埃云，阻挡了太阳光，使冰层的融化慢下来。\n所以说火星天气太恶劣了，'
                                  '去过一次就不想再去第二次了')
    else:
        msg = await get_weather_of_city(city)

    name = event.sender.card
    if name == "":
        name = event.sender.nickname
    log = f'{name}（{event.user_id}，{event.group_id}） - 查询天气：{city}'
    logger.info(log)
    await weather.finish(msg)


def _get_city(message_str: str) -> str:
    '''
    :说明
        匹配消息中的城市名称

    :参数
        * message_str：原始消息

    :返回
        * str：天气city
    '''

    # 匹配前面
    args = re.search(r'[\u4e00-\u9fa5]+[天气]$', message_str)
    if args is not None:
        # 获得字符串
        loc = re.search('天气', args.string).span()[0]
        args = args.string[0:loc]
        # 去除前缀
        head = re.search(r'(查一下)|(问一下)|(问问)|(想知道)|(查询)|(查查)', args)
        if head is not None:
            loc = head.span()[1]
            args = args[loc:]
        return args
    else:
        # 匹配后面
        loc = re.search('天气 ', message_str).span()[1]
        return message_str[loc:]
