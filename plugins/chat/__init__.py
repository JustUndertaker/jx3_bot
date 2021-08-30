from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.cqhttp.permission import GROUP

from nonebot.typing import T_State
from utils.log import logger
from .data_source import get_chat_reply

from nonebot.plugin import export

export = export()
export.plugin_name = '闲聊'
export.plugin_usage = '普普通通的闲聊\n命令：@robot闲聊内容'

chat = on_message(rule=to_me(), permission=GROUP, priority=8, block=True)


@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    自动根据确定API
    '''
    # 获得聊天内容
    text = event.get_plaintext()
    name = event.sender.card
    if name == '':
        name = event.sender.nickname
    flag = True
    log = f'{name}（{event.user_id}，{event.group_id}）：{text}'
    logger.info(log)
    try:
        msg = await get_chat_reply(text)
    except Exception:
        f'{name}（{event.user_id}，{event.group_id}）：闲聊失败。'
        logger.error(log)
        flag = False

    if flag:
        await chat.finish(msg)
    else:
        await chat.finish()
