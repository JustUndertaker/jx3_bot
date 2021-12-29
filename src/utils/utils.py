from typing import Union

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


class GroupList_Async():
    '''异步计数器，用于群发消息，支持list[int]和list[dict]，返回的是group_id'''

    def __init__(self, obj: Union[list, dict]):
        if isinstance(obj[0], int):
            self._it = iter(obj)
            return
        if isinstance(obj[0], dict):
            group_id_list = [one['group_id'] for one in obj]
            self._it = iter(group_id_list)

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
