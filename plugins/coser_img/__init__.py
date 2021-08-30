import re
from httpx import RequestError, HTTPStatusError
from nonebot import on_regex
from nonebot.exception import ActionFailed

from .moe import img_from_moe
from .rosysun import img_from_rosysun
from .yanghanwen import img_from_yanghanwen
from utils.log import logger
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.plugin import export

export = export()
export.plugin_name = 'cos'
export.plugin_usage = '获得好看的小姐姐\n命令：cos/coser'

_reg_pattern = r'^[cC][oO][sS](er)?$'
coser = on_regex(_reg_pattern, priority=5, block=True)
_api = [
    img_from_yanghanwen,
    img_from_moe,
    img_from_rosysun,
]


@coser.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 只匹配cos纯指令(或coser，前三个字母不分大小写)，后续带任何字符都不作处理
    text = event.get_plaintext()
    matcher = re.match(_reg_pattern, text)
    if matcher is None:
        return
    message = None
    for api in _api:
        try:
            message = api()
            break
        except (RequestError, HTTPStatusError) as httpExc:
            logger.error(f'{export.plugin_name}插件访问网络异常: {httpExc}')
            continue
        except Exception as e:
            logger.error(f'{export.plugin_name}插件异常: {e}')
            continue
    if message is None:
        await coser.finish('无法获取正确图片')
        return
    try:
        # 由于图片可能无法访问，因此需要捕捉ActionFailed异常
        await coser.finish(message)
    except ActionFailed:
        await coser.finish('图片获取失败')
