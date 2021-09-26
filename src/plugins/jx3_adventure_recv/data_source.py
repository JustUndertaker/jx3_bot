import os

from modules.group_info import GroupInfo
from modules.plugin_info import PluginInfo


async def get_server(group_id: int) -> str:
    '''
    获取绑定服务器名称
    '''
    return await GroupInfo.get_server(group_id)


async def get_robot_status(group_id: int) -> bool:
    '''获取机器人状态'''

    robot_status = await GroupInfo.get_robot_status(group_id)
    _, self_module = os.path.split(os.path.split(__file__)[0])
    plugin_status = await PluginInfo.get_status(self_module, group_id)

    return (robot_status and plugin_status)
