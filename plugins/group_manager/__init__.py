from nonebot import get_driver
from nonebot.plugin import export
from nonebot.adapters.cqhttp import Bot
from .data_source import group_init

export = export()
export.plugin_name = '群管理'
export.plugin_usage = '用于操作群相关管理。'
export.ignore = True  # 插件管理器忽略此插件


driver = get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    '''
    初始化注册群
    '''
    group_list = await bot.get_group_list()
    for group in group_list:
        await group_init(group['group_id'])
