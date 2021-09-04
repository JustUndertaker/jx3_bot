from modules.group_info import GroupInfo
from typing import Optional
import httpx
from utils.user_agent import get_user_agent


async def group_init(group_id: int) -> None:
    '''
    注册群信息
    '''
    await GroupInfo.append_or_update(group_id)


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
