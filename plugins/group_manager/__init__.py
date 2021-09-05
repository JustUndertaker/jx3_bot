from nonebot import get_driver, on_regex, on_notice
from nonebot.plugin import export
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    MessageSegment,
)
from configs.config import DEFAULT_WELCOME, DEFAULT_LEFT, DEFAULT_LEFT_KICK, DEFAULT_STATUS
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from utils.log import logger
from utils.utils import get_admin_list, nickname
from .data_source import (
    group_init,
    user_init,
    get_server_name,
    change_server,
    change_active,
    check_event,
    check_robot_status,
    user_detele,
    get_user_name,
    group_detel,
)

export = export()
export.plugin_name = '群管理'
export.plugin_usage = '用于操作群相关管理。'
export.ignore = True  # 插件管理器忽略此插件


driver = get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    '''
    初始化注册
    '''
    # 群注册
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group['group_id']
        await group_init(group_id=group_id)
        # 用户注册
        user_list = await bot.get_group_member_list(group_id=group_id)
        for user in user_list:
            user_id = user['user_id']
            user_name = user['nickname'] if user['card'] == "" else user['card']
            await user_init(user_id, group_id, user_name)

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
        log = '更换服务器出错，参数错误。'
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


check_in_group = ['notice.group_increase.approve', 'notice.group_increase.invite']
someone_in_group = on_notice(rule=check_event(check_in_group), priority=3, block=True)


@someone_in_group.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    '''
    群成员增加事件
    '''
    group_id = event.group_id
    user_id = event.user_id
    self_id = event.self_id
    # 判断是否是机器人进群
    if user_id == self_id:
        # 注册群
        await group_init(group_id)
        # 用户注册
        user_list = await bot.get_group_member_list(group_id=group_id)
        for user in user_list:
            user_id = user['user_id']
            user_name = user['nickname'] if user['card'] == "" else user['card']
            await user_init(user_id, group_id, user_name)

            msg = f'我加入了群({group_id})'
            admin_user_list = get_admin_list()
            for admin_id in admin_user_list:
                await bot.send_private_msg(user_id=admin_id, message=msg)
        msg = None
        if DEFAULT_STATUS:
            msg = f'可爱的{nickname}驾到了，有什么问题尽管来问我吧！'
        await someone_in_group.finish(msg)

    # 判断机器人是否开启
    status = await check_robot_status(group_id)
    if status is None or status is False:
        await someone_in_group.finish()

    # 注册用户
    user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=True)
    user_name = user_info['nickname']
    await user_init(user_id, group_id, user_name)
    # 欢迎语
    msg = MessageSegment.at(user_id)+DEFAULT_WELCOME
    await someone_in_group.finish(msg)


check_left = ['notice.group_decrease.leave', 'notice.group_decrease.kick', 'notice.group_decrease.kick_me']
someone_left = on_notice(rule=check_event(check_left), priority=3, block=True)


@someone_left.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    '''
    群成员减少事件
    '''
    user_id = event.user_id
    group_id = event.group_id
    user_name = await get_user_name(user_id, group_id)
    # 删除数据
    await user_detele(user_id, group_id)

    sub_type = event.sub_type
    if sub_type == "kick_me":
        # 机器人被踢了
        msg = f'我在群({group_id})被管理员踹走了……'
        admin_user_list = get_admin_list()
        for admin_id in admin_user_list:
            await bot.send_private_msg(user_id=admin_id, message=msg)
        # 删除数据
        await group_detel(group_id)
        await someone_in_group.finish()

    # 查看群是否开启
    status = await check_robot_status(group_id)
    if status is None or status is False:
        await someone_in_group.finish()

    sub_type = event.sub_type
    if sub_type == "leave":
        # 有人主动退群
        msg = f"{user_name}({user_id})"+DEFAULT_LEFT
        await someone_in_group.finish(msg)

    if sub_type == "kick":
        # 有人被踢出群
        msg = f"{user_name}({user_id})"+DEFAULT_LEFT_KICK
        await someone_in_group.finish(msg)

    await someone_in_group.finish()
