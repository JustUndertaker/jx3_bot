from nonebot import get_driver, on_regex
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent
from nonebot.adapters.cqhttp.permission import PRIVATE_FRIEND
from nonebot.plugin import export
from src.utils.config import config
from src.utils.log import logger
from src.utils.scheduler import scheduler

from .data_source import (bot_connect, bot_disconnect, clean_bot,
                          clean_bot_owner, set_bot_owner)

export = export()
export.plugin_name = 'bot管理插件'
export.plugin_usage = '用于bot的管理'
export.ignore = True  # 插件管理器忽略此插件

driver = get_driver()

outtime: int = config.get('default').get('bot-outtime')


@driver.on_bot_connect
async def _(bot: Bot):
    '''
    链接bot
    '''
    bot_id = int(bot.self_id)
    log = f'连接到bot（{bot.self_id}），正在注册信息'
    logger.info(log)
    await bot_connect(bot_id)
    log = f'bot（{bot.self_id}）信息注册完毕'
    logger.info(log)


@driver.on_bot_disconnect
async def _(bot: Bot):
    '''
    机器人断开链接
    '''
    bot_id = int(bot.self_id)
    log = f'检测到bot（{bot.self_id}）断开链接.'
    logger.info(log)
    await bot_disconnect(bot_id)


# 定时清理离线超过时间的Bot
@scheduler.scheduled_job("cron", hour=23, minute=59)
async def _():
    log = '正在清理离线bot'
    logger.info(log)
    count = await clean_bot()
    log = f'清理完毕，本次共清理 {count} 个机器人数据'
    logger.info(log)


# 设置管理员
set_owner = on_regex(pattern=r"^设置管理员$", permission=PRIVATE_FRIEND, priority=2, block=True)


@set_owner.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''私聊设置管理员'''
    bot_id = int(bot.self_id)
    owner_id = event.user_id
    nickname = event.sender.nickname
    flag = await set_bot_owner(bot_id, owner_id)
    if flag is None:
        msg = "设置失败，机器人记录不存在。"
    elif flag:
        msg = f'设置成功，当前管理员为：{nickname}（{owner_id}）'
    else:
        msg = "设置失败，该机器人已有管理员。\n如需要更换管理员，请管理员账号输入：清除管理员"
    await set_owner.finish(msg)


# 清除管理员
clean_owner = on_regex(pattern=r"^清除管理员$", permission=PRIVATE_FRIEND, priority=2, block=True)


@clean_owner.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''清除管理员'''
    bot_id = int(bot.self_id)
    owner_id = event.user_id
    flag = await clean_bot_owner(bot_id, owner_id)
    if flag is None:
        msg = "没有什么好清除的了。"
    elif flag:
        msg = "清除成功，可以重新设置管理员了。"
    else:
        msg = "清除失败惹，你不是管理员。"
    await clean_owner.finish(msg)
