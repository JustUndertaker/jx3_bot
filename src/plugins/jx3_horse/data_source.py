from src.modules.group_info import GroupInfo


async def get_server(bot_id: int, group_id: int) -> str:
    '''
    获取绑定服务器名称
    '''
    return await GroupInfo.get_server(bot_id, group_id)
