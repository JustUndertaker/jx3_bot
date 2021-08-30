import json
import random

import re
from httpx import RequestError, HTTPStatusError
from nonebot import on_regex
from nonebot.exception import ActionFailed

from utils.log import logger
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from .lolicon import fetch_lolicon_random_img

from nonebot.plugin import export

export = export()
export.plugin_name = '色图'
export.plugin_usage = '获得lolicon的涩图\n命令：色图/涩图'


_reg_pattern = r'^[色|涩]图$'
sexy_img = on_regex(_reg_pattern, priority=5, block=True)

"""
    注意所有获取图片的api，其返回格式必须符合
    title author url
"""
_random_api = [
    fetch_lolicon_random_img
]


@sexy_img.handle()
async def _(bot: Bot, event: Event, state: T_State):
    text = event.get_plaintext()
    matcher = re.match(_reg_pattern, text)
    # 当前色图插件只支持纯指令(避免和搜/识图插件的指令混淆)
    if matcher is not None:
        try:
            api = _get_random_api()
            (title, author, url) = await api()
            text = MessageSegment.text(f'标题: {title}\n画师: {author}\n地址: {url}\n')
            img = MessageSegment.image(url)
            message = text + img
            logger.info(f'涩图插件发送: {message}')
        except (RequestError, HTTPStatusError) as httpExc:
            logger.error(f'涩图插件访问网络异常: {httpExc}')
            message = MessageSegment.text('网络异常')
        except json.JSONDecodeError as jsonExc:
            logger.error(f'涩图插件接口返回数据结构异常: {jsonExc}')
            message = MessageSegment.text('返回异常')
        except Exception as e:
            logger.error(f'涩图插件异常: {e}')
            message = MessageSegment.text('其余异常')
        try:
            # 由于图片可能无法访问，因此需要捕捉ActionFailed异常
            await sexy_img.finish(message)
        except ActionFailed:
            await sexy_img.finish('信息发送失败')


# 返回随机获取图片的随机一个api
def _get_random_api():
    api = _random_api[random.randint(0, len(_random_api) - 1)]
    return api
