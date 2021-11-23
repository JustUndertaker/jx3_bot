from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.permission import Permission
from src.modules.bot_info import BotInfo


async def get_nickname(bot_id: int) -> str:
    '''获取昵称'''
    return await BotInfo.get_nickname(bot_id)


async def _owner(bot: "Bot", event: "Event"):
    bot_id = int(bot.self_id)
    user_id = int(event.get_user_id())
    owner_id = await BotInfo.get_owner(bot_id)
    return (user_id == owner_id)

OWNER = Permission(_owner)
'''匹配消息是否是机器人的管理员'''
