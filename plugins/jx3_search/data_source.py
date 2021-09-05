from modules.group_info import GroupInfo
from .config import zhiye_name
import re


async def get_server(group_id: int) -> str:
    '''
    获取绑定服务器名称
    '''
    return await GroupInfo.get_server(group_id)


def get_macro_name(text: str) -> str:
    '''宏查询返回职业'''
    args = re.search(r'^[\u4e00-\u9fa5]+宏$', text)
    if args is not None:
        return text[:-1]
    else:
        return text.split(' ')[-1]


def get_xinfa(name: str) -> str:
    '''获取心法名称'''
    for key, xinfa in zhiye_name.items():
        for one_name in xinfa:
            if one_name == name:
                return key

    # 未找到，返回原值
    return name
