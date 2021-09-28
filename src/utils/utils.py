import nonebot
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.permission import Permission
from src.modules.bot_info import BotInfo

nickname = list(nonebot.get_driver().config.nickname)[0]
'''机器人昵称'''


async def _owner(bot: "Bot", event: "Event"):
    bot_id = int(bot.self_id)
    user_id = int(event.get_user_id())
    owner_id = await BotInfo.get_owner(bot_id)
    return (user_id == owner_id)

OWNER = Permission(_owner)
'''匹配消息是否是机器人的管理员'''


def get_bot():
    '''
    全局获取bot对象
    '''
    return list(nonebot.get_bots().values())[0]
