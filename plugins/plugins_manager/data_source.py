from typing import Optional
from nonebot.adapters.cqhttp import MessageSegment

from utils.utils import nickname
from .model import PluginManager
from modules.plugin_info import PluginInfo
from modules.group_info import GroupInfo


async def check_group_init(group_id: int,module_name:str) -> bool:
    '''
    :说明
        检查群是否注册，会跳过忽略插件

    :参数
        * group_id：QQ群号
        * module_name：模块名

    :返回
        * bool：是否注册
    '''
    for plugin in PluginManager:
        if module_name==plugin.module_name:
            if plugin.ignore:
                return False
    return await GroupInfo.check_group_init(group_id)


async def check_plugin_status(module_name: str, group_id: int) -> Optional[bool]:
    '''
    :说明
        查看插件状态

    :参数
        * module_name：插件模块名
        * group_id：QQ群号

    :返回
        * bool:插件状态
    '''
    # 判断机器人开关
    status = await GroupInfo.get_robot_status(group_id)
    if status is None or status is False:
        return False
    # 返回插件开关
    return await PluginInfo.get_status(module_name, group_id)


async def plugin_init(group_id: int) -> None:
    '''
    :说明
        注册一个群的所有插件
    '''
    for plugin in PluginManager:
        # 跳过忽略的插件
        if plugin.ignore:
            continue
        module_name = plugin.module_name
        description = plugin.plugin_usage
        await PluginInfo.append_or_update(module_name, description, group_id)


async def change_plugin_status(plugin_name: str, group_id: int, status: bool) -> MessageSegment:
    '''
    :说明
        设置插件状态

    :参数
        * plugin_name：插件名
        * group_id：QQ群号
        * status：状态

    :返回
        * MessageSegment消息
    '''
    # 获取module_name
    module_name = None
    for plugin in PluginManager:
        if plugin.plugin_name == plugin_name:
            module_name = plugin.module_name
            break

    if module_name is not None:
        await PluginInfo.change_status(module_name, group_id, status)
        if status:
            msg = MessageSegment.text(f'插件[{plugin_name}]当前状态为：开启')
        else:
            msg = MessageSegment.text(f'插件[{plugin_name}]当前状态为：关闭')
    else:
        msg = MessageSegment.text(f'未找到插件[{plugin_name}]。')

    return msg


async def get_meau_data(self_id: int, group_id: int) -> dict:
    '''
    :说明
        获取机器人状态数据

    :参数
        * self_id：机器人QQ
        * group_id：QQ群号

    :返回
        * dict
    '''
    plugin_list_db = await PluginInfo.get_all_status_from_group(group_id)

    # 构造字典列表
    plugin_list: list[dict] = []
    for plugin_db in plugin_list_db:
        data = {}
        for plugin_manager in PluginManager:
            if plugin_manager.module_name == plugin_db['module_name']:
                data['name'] = plugin_manager.plugin_name
                data['des'] = plugin_db['description']
                data['status'] = plugin_db['status']
        plugin_list.append(data)

    alldata = {}
    alldata['plugins'] = plugin_list

    robot_status = await GroupInfo.get_robot_status(group_id)
    if robot_status:
        alldata['robot_status'] = "开"
    else:
        alldata['robot_status'] = "关"
    server = await GroupInfo.get_server(group_id)
    alldata['server'] = server
    sign_nums = await GroupInfo.get_sign_nums(group_id)
    alldata['sign_nums'] = sign_nums
    active = await GroupInfo.get_active(group_id)
    alldata['active'] = active

    alldata['nickname'] = nickname
    alldata['head_icon'] = f'http://q1.qlogo.cn/g?b=qq&nk={str(self_id)}&s=640'

    return alldata
