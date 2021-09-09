from modules.group_info import GroupInfo
from modules.user_info import UserInfo
from typing import Tuple
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.rule import Rule


def check_event(event_list: str):
    '''
    检查事件
    '''

    async def _check_event(bot: "Bot", event: "Event", state: T_State) -> bool:
        return event.get_event_name() in event_list

    return Rule(_check_event)


async def set_robot_status(group_id: int, status: bool) -> bool:
    '''设置机器人开关'''
    return await GroupInfo.set_robot_status(group_id, status)


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


async def change_status_all(status: bool) -> None:
    '''设置所有状态'''
    await GroupInfo.change_status_all(status)


async def leave_group(group_id: int) -> Tuple[bool, str]:
    '''退群，返回[成功flag，群名]'''
    group_name = await GroupInfo.get_group_name(group_id)
    if group_name is None:
        group_name = ""
        return False, group_name

    await GroupInfo.delete_one(group_id=group_id)
    await UserInfo.delete_group(group_id)
    return True, group_name
