from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export
from src.utils.config import config
from src.utils.log import logger
from src.utils.scheduler import scheduler

from .data_source import bot_connect, bot_disconnect, clean_bot

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
