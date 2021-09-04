from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.rule import to_me
from nonebot import on_message
from nonebot.plugin import export
from utils.log import logger
from .data_source import get_reply_jx3, get_reply_qingyunke

export = export()
export.plugin_name = '智能闲聊'
export.plugin_usage = '让机器人开启聊天功能。'
export.ignore = False  # 插件管理器忽略此插件


chat = on_message(rule=to_me(), permission=GROUP, priority=8, block=True)


@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    自动根据确定API
    '''
    # 获得聊天内容
    text = event.get_plaintext()
    name = event.sender.nickname if event.sender.card == "" else event.sender.card
    log = f'{name}（{event.user_id}，{event.group_id}）闲聊：{text}'
    logger.info(log)

    # 使用jx3api访问
    msg = await get_reply_jx3(text)
    if msg is None:
        # 使用青云客访问
        msg = await get_reply_qingyunke(text)
        if msg is None:
            # 访问失败
            log = '接口访问失败，关闭事件。'
            logger.info(log)
            await chat.finish()

    log = f'接口返回：{msg}'
    logger.info(log)
    await chat.finish(msg)
