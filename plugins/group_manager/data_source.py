from modules.group_info import GroupInfo


async def group_init(group_id: int) -> None:
    '''
    注册群信息
    '''
    await GroupInfo.append_or_update(group_id)
