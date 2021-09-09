from modules.group_info import GroupInfo
from modules.user_info import UserInfo
from typing import Optional
import httpx
from nonebot.typing import T_State
from utils.user_agent import get_user_agent
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.rule import Rule


async def group_init(group_id: int, group_name: str) -> None:
    '''
    注册群信息
    '''
    await GroupInfo.append_or_update(group_id, group_name)


async def get_group_name(group_id: int) -> str:
    '''获取群名'''
    return await GroupInfo.get_group_name(group_id)


async def group_detel(group_id: int) -> None:
    '''删除群数据'''
    await GroupInfo.delete_one(group_id)
    await UserInfo.delete_group(group_id)


async def user_init(user_id: int, group_id: int, user_name: str) -> None:
    '''
        :说明
            注册一条用户信息

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * user_name：用户昵称
    '''
    await UserInfo.append_or_update(user_id, group_id, user_name)


async def user_detele(user_id: int, group_id: int) -> None:
    '''
    删除成员信息
    '''
    await UserInfo.delete_one(user_id, group_id)


async def get_user_name(user_id: int, group_id: int) -> str:
    '''
    获取用户名称
    '''
    name = await UserInfo.get_user_name(user_id, group_id)
    return name


async def change_server(group_id: int, server: str) -> None:
    '''
    :说明
        更换绑定服务器

    :参数
        * group_id：QQ群号
        * server：服务器
    '''
    await GroupInfo.set_server(group_id, server)


async def get_server_name(name: str) -> Optional[str]:
    '''
    根据服务器获取主服务器名
    '''
    url = 'https://www.jx3api.com/app/master'
    params = {"name": name}
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        req_url = await client.get(url=url, params=params)
        req = req_url.json()
    code = req.get('code')
    if code == 200:
        data = req['data']
        return data['server']
    else:
        return None


async def change_active(group_id: int, active: int) -> None:
    '''
    设置活跃值
    '''
    await GroupInfo.set_active(group_id, active)


def check_event(event_list: str):
    '''
    检查事件
    '''

    async def _check_event(bot: "Bot", event: "Event", state: T_State) -> bool:
        return event.get_event_name() in event_list

    return Rule(_check_event)


async def check_robot_status(group_id: int) -> Optional[bool]:
    '''
    :说明
        检查机器人状态

    :参数
        * group_id：QQ群号

    :返回
        * bool：开关状态
        * None：未注册群
    '''
    return await GroupInfo.get_robot_status(group_id)


async def set_robot_status(group_id: int, status: bool) -> bool:
    '''设置机器人开关'''
    return await GroupInfo.set_robot_status(group_id, status)
