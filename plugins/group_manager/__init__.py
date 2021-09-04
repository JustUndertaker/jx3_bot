from nonebot import get_driver, on_regex
from nonebot.plugin import export
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from utils.log import logger
from .data_source import (
    group_init,
    get_server_name,
    change_server,
    change_active
)

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

server_regex = r"^服务器 [\u4e00-\u9fa5]+$"
server_useage = "[更换绑定服务器]\n群管理命令：服务器 XXX"
server_change = on_regex(pattern=server_regex, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)


@server_change.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    管理员绑定服务器
    '''
    regex = event.get_plaintext()
    name = regex.split(' ')[-1]
    playername = event.sender.nickname if event.sender.card == "" else event.sender.card
    group_id = event.group_id
    log = f'[{playername}]({event.user_id},{group_id})更换服务器，参数：{name}'
    logger.info(log)
    server = await get_server_name(name)
    if server is None:
        msg = f'参数错误，检查一下呀。\n{server_useage}'
        log = f'更换服务器出错，参数错误。'
        logger.info(log)
        await server_change.finish(msg)
    await change_server(group_id=group_id, server=server)
    msg = f'当前绑定服务器为：{server}'
    log = f'更换服务器成功，绑定服务器为：{server}'
    logger.info(log)
    await server_change.finish(msg)


active_regex = r"^活跃值 [0-9]+$"
active_usage = "[设置活跃值]\n群管理命令：活跃值 XX（1-99）"
active_change = on_regex(pattern=server_regex, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)


@active_change.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    设置活跃值
    '''
    regex = event.get_plaintext()
    active = int(regex.split(' ')[-1])
    if active < 1 or active > 99:
        msg = f"参数错误，检查一下呀。\n{active_usage}"
        await active_change.finish(msg)

    group_id = event.group_id
    await change_active(group_id, active)
    msg = f"活跃值设为：{active}"
    await active_change.finish(msg)
