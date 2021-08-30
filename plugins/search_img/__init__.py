from enum import Enum

from httpx import RequestError, HTTPStatusError
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.typing import T_State
from utils.log import logger

from .pixiv import pixiv_search

from nonebot.plugin import export

export = export()
export.plugin_name = '识图'
export.plugin_usage = '用于P站识图功能\n命令：p站识图/P站识图'


class Option(Enum):
    pixiv = 1


search_img = on_command('识图', priority=5, block=True)
"""
    api接口返回必须为MessageSegment数组
"""
_search_api = {
    Option.pixiv: pixiv_search
}


@search_img.args_parser
@search_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    message = event.message
    if len(message) >= 1:
        state['option'] = Option.pixiv
        state['img_url'] = message[0].data.get('url', None)


@search_img.got('img_url', prompt='图呢?')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    option = state.get('option', '')
    img_url = state['img_url'].strip()
    await search_img.send('正在识别...')
    try:
        messages = _search_api[option](img_url)
        for message in messages:
            await search_img.send(message)
    except (RequestError, HTTPStatusError) as httpExc:
        logger.error(f'{export.plugin_name}插件访问网络异常: {httpExc}')
        await search_img.send('网络异常')
    except Exception as e:
        logger.error(f'{export.plugin_name}插件异常: {e}')
        await search_img.send('其余异常')
    finally:
        await search_img.finish('识别完毕')
