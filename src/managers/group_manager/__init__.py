from nonebot import get_driver, on_notice, on_regex
from nonebot.adapters.cqhttp import (Bot, GroupDecreaseNoticeEvent,
                                     GroupIncreaseNoticeEvent,
                                     GroupMessageEvent, MessageSegment)
from nonebot.adapters.cqhttp.permission import GROUP, GROUP_ADMIN, GROUP_OWNER
from nonebot.plugin import export
from src.utils.config import config as baseconfig
from src.utils.log import logger
from src.utils.utils import OWNER, nickname

from ..plugins_manager.data_source import plugin_init
from . import data_source as source

export = export()
export.plugin_name = '群管理'
export.plugin_command = ""
export.plugin_usage = '用于操作群相关管理。'
export.default_status = True  # 插件默认开关
export.ignore = True  # 插件管理器忽略此插件

config = baseconfig.get('default')

driver = get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    '''
    初始化注册
    '''
    # 群注册
    bot_id = int(bot.self_id)
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group['group_id']
        group_name = group['group_name']
        await source.group_init(bot_id=bot_id, group_id=group_id, group_name=group_name)
        # 用户注册
        user_list = await bot.get_group_member_list(group_id=group_id)
        for user in user_list:
            user_id = user['user_id']
            user_name = user['nickname'] if user['card'] == "" else user['card']
            await source.user_init(bot_id, user_id, group_id, user_name)

# 绑定服务器
server_regex = r"^绑定 [\u4e00-\u9fa5]+$"
server_change = on_regex(pattern=server_regex, permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)
# 设置活跃值
active_regex = r"^活跃值 [0-9]+$"
active_change = on_regex(pattern=active_regex, permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)
# 群成员增加事件
check_in_group = ['notice.group_increase.approve', 'notice.group_increase.invite']
someone_in_group = on_notice(rule=source.check_event(check_in_group), priority=3, block=True)
# 群成员减少事件
check_left = ['notice.group_decrease.leave', 'notice.group_decrease.kick', 'notice.group_decrease.kick_me']
someone_left = on_notice(rule=source.check_event(check_left), priority=3, block=True)
# 机器人开关
robotregex = r'^机器人 [开|关]$'
robotchange = on_regex(pattern=robotregex, permission=OWNER, priority=2, block=True)
# 滴滴管理员
didi_admin = on_regex(pattern=r"^滴滴 ", permission=GROUP, priority=5, block=True)


@server_change.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    管理员绑定服务器
    '''
    bot_id = int(bot.self_id)
    regex = event.get_plaintext()
    name = regex.split(' ')[-1]
    playername = event.sender.nickname if event.sender.card == "" else event.sender.card
    group_id = event.group_id
    log = f'Bot({bot.self_id}) | [{playername}]({event.user_id},{group_id})更换服务器，参数：{name}'
    logger.info(log)
    server = await source.get_server_name(name)
    if server is None:
        msg = '参数错误，检查一下呀。\n[更换绑定服务器]\n群管理命令：绑定 XXX'
        log = '更换服务器出错，参数错误。'
        logger.info(log)
        await server_change.finish(msg)
    await source.change_server(bot_id=bot_id, group_id=group_id, server=server)
    msg = f'当前绑定服务器为：{server}'
    log = f'更换服务器成功，绑定服务器为：{server}'
    logger.info(log)
    await server_change.finish(msg)


@active_change.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    设置活跃值
    '''
    bot_id = int(bot.self_id)
    regex = event.get_plaintext()
    active = int(regex.split(' ')[-1])
    if active < 1 or active > 99:
        msg = "参数错误，检查一下呀。\n[设置活跃值]\n群管理命令：活跃值 XX（1-99）"
        await active_change.finish(msg)

    group_id = event.group_id
    await source.change_active(bot_id, group_id, active)
    msg = f"活跃值设为：{active}"
    log = f"Bot({bot.self_id}) | 群[{group_id}]设置活跃值：{active}"
    logger.info(log)
    await active_change.finish(msg)


@someone_in_group.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    '''
    群成员增加事件
    '''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    user_id = event.user_id
    self_id = event.self_id
    # 判断是否是机器人进群
    if user_id == self_id:
        # 注册群
        group_info = await bot.get_group_info(group_id=group_id, no_cache=True)
        group_name = group_info['group_name']
        await source.group_init(bot_id, group_id, group_name)
        # 用户注册
        user_list = await bot.get_group_member_list(group_id=group_id)
        # 插件注册
        await plugin_init(bot_id, group_id)
        for user in user_list:
            user_id = user['user_id']
            user_name = user['nickname'] if user['card'] == "" else user['card']
            await source.user_init(bot_id, user_id, group_id, user_name)

        msg = f'我加入了群[{group_name}]({group_id})'
        owner_id = await source.get_bot_owner(bot_id)
        if owner_id is not None:
            await bot.send_private_msg(user_id=owner_id, message=msg)
        msg = None
        defaule_status: bool = config.get('robot-status')
        if defaule_status:
            msg = f'可爱的{nickname}驾到了，有什么问题尽管来问我吧！'
        await someone_in_group.finish(msg)

    # 判断机器人是否开启
    status = await source.check_robot_status(bot_id, group_id)
    if status is None or status is False:
        await someone_in_group.finish()

    # 注册用户
    user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=True)
    user_name = user_info['nickname']
    await source.user_init(bot_id, user_id, group_id, user_name)
    # 欢迎语
    default_welcome: str = config.get('robot-welcome')
    msg = MessageSegment.at(user_id)+default_welcome
    await someone_in_group.finish(msg)


@someone_left.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    '''
    群成员减少事件
    '''
    bot_id = int(bot.self_id)
    user_id = event.user_id
    group_id = event.group_id
    user_name = await source.get_user_name(bot_id, user_id, group_id)
    # 删除数据
    await source.user_detele(bot_id, user_id, group_id)

    sub_type = event.sub_type
    if sub_type == "kick_me":
        # 机器人被踢了
        group_name = await source.get_group_name(bot_id, group_id)
        msg = f'我在[{group_name}]({group_id})被管理员踹走了……'
        owner_id = await source.get_bot_owner(bot_id)
        if owner_id is not None:
            await bot.send_private_msg(user_id=owner_id, message=msg)
        # 删除数据
        await source.group_detel(bot_id, group_id)
        await someone_in_group.finish()

    # 查看群是否开启
    status = await source.check_robot_status(bot_id, group_id)
    if status is None or status is False:
        await someone_in_group.finish()

    sub_type = event.sub_type
    if sub_type == "leave":
        # 有人主动退群
        default_left: str = config.get('robot-someone-left')
        msg = f"{user_name}({user_id})"+default_left
        await someone_in_group.finish(msg)

    if sub_type == "kick":
        # 有人被踢出群
        default_kick: str = config.get('robot-left-kick')
        msg = f"{user_name}({user_id})"+default_kick
        await someone_in_group.finish(msg)

    await someone_in_group.finish()


@robotchange.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    设置机器人状态
    '''
    bot_id = int(bot.self_id)
    get_status = event.get_plaintext().split(" ")[-1]
    group_id = event.group_id
    if get_status == "开":
        status = True
    else:
        status = False

    # 设置开关
    await source.set_robot_status(bot_id, group_id, status)
    msg = f"{nickname} 当前状态为：[{get_status}]"
    await robotchange.finish(msg)


@didi_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    滴滴管理员，给管理员发送消息
    '''
    bot_id = int(bot.self_id)
    _msg = event.get_plaintext()[3:]
    # 获取管理员
    owner = await source.get_bot_owner(bot_id)

    if owner is None:
        msg = f"{nickname} 目前还没有管理呢，不知道发给谁。"
        await didi_admin.finish(msg)

    group_id = str(event.group_id)
    group_info = await bot.get_group_info(group_id=event.group_id, no_cache=False)
    group_name = group_info.get("group_name")
    user_id = str(event.user_id)
    user_name = event.sender.nickname
    msg = f"收到群 {group_name}({group_id}) 内 {user_name}({user_id}) 的滴滴消息：\n\n{_msg}"
    await bot.send_private_msg(user_id=owner, message=msg)
    reply = "消息已发送给管理员了……"
    await didi_admin.finish(reply)
