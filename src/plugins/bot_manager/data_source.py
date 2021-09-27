from datetime import datetime, timedelta

from src.modules.bot_info import BotInfo
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo
from src.modules.user_info import UserInfo
from src.utils.log import logger


async def bot_connect(bot_id: int) -> None:
    '''链接机器人'''
    await BotInfo.bot_connect(bot_id)


async def bot_disconnect(bot_id: int) -> None:
    '''机器人断开链接'''
    await BotInfo.bot_disconnect(bot_id)


async def clean_bot(outtime: int) -> int:
    '''清理bot数据，返回清理bot数量'''
    bot_list = await BotInfo.get_disconnect_bot()
    nowtime = datetime.now()
    count = 0
    for bot in bot_list:
        bot_id = bot.get('bot_id')
        last_left: datetime = bot.get('last_left')+timedelta(hours=outtime)
        if nowtime > last_left:
            await _clean_bot(bot_id)
            count += 1
    return count


async def _clean_bot(bot_id: int) -> None:
    '''清理Bot数据'''
    log = f'bot（{str(bot_id)}）正在清理表：bot_info'
    logger.debug(log)
    await BotInfo.detele_bot(bot_id)
    log = f'bot（{str(bot_id)}）正在清理表group_info'
    logger.debug(log)
    await GroupInfo.detele_bot(bot_id)
    log = f'bot（{str(bot_id)}）正在清理表plugin_info'
    logger.debug(log)
    await PluginInfo.detele_bot(bot_id)
    log = f'bot（{str(bot_id)}）正在清理表user_info'
    logger.debug(log)
    await UserInfo.detele_bot(bot_id)
    log = f'bot（{str(bot_id)}）数据清理完毕'
    logger.debug(log)
