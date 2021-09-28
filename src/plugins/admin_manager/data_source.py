from typing import Optional, Tuple

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.rule import Rule
from nonebot.typing import T_State
from src.modules.bot_info import BotInfo
from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo


def check_event(event_list: list[str]):
    '''
    检查事件
    '''

    async def _check_event(bot: "Bot", event: "Event", state: T_State) -> bool:
        return event.get_event_name() in event_list

    return Rule(_check_event)


async def get_bot_owner(bot_id: int) -> Optional[int]:
    '''获取机器人管理员账号'''
    owner = await BotInfo.get_owner(bot_id)
    return owner


async def set_robot_status(bot_id: int, group_id: int, status: bool) -> bool:
    '''设置机器人开关'''
    return await GroupInfo.set_robot_status(bot_id, group_id, status)


async def get_all_data() -> list[dict]:
    '''
        :返回所有数据,dict字段：
        * group_id：群号
        * group_name：群名
        * sign_nums：签到数
        * server：服务器名
        * robot_status：运行状态
        * active：活跃值
    '''
    return await GroupInfo.get_all_data()


def get_text_num(text: str) -> Tuple[bool, int]:
    '''从信息中获取开关，群号'''
    _status = text.split(' ')[0]
    _group_id = text.split(' ')[1]
    status = (_status == "打开")
    group_id = int(_group_id)
    return status, group_id


async def change_status_all(bot_id: int, status: bool) -> None:
    '''设置所有状态'''
    await GroupInfo.change_status_all(bot_id, status)


async def leave_group(bot_id: int, group_id: int) -> Tuple[bool, str]:
    '''退群，返回[成功flag，群名]'''
    group_name = await GroupInfo.get_group_name(bot_id, group_id)
    if group_name is None:
        group_name = ""
        return False, group_name

    await GroupInfo.delete_one(bot_id=bot_id, group_id=group_id)
    await UserInfo.delete_group(bot_id=bot_id, group_id=group_id)
    return True, group_name
