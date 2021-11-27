import asyncio
import random
import time

from nonebot import get_bots, on_notice, on_regex
from nonebot.adapters.cqhttp import (Bot, GroupDecreaseNoticeEvent,
                                     GroupIncreaseNoticeEvent,
                                     GroupMessageEvent, MessageSegment)
from nonebot.adapters.cqhttp.permission import GROUP, GROUP_ADMIN, GROUP_OWNER
from nonebot.plugin import export
from src.utils.browser import get_html_screenshots
from src.utils.config import config as baseconfig
from src.utils.log import logger
from src.utils.scheduler import scheduler
from src.utils.utils import OWNER, get_nickname

from ..plugins_manager.data_source import plugin_init
from . import data_source as source

export = export()
export.plugin_name = '群管理'
export.plugin_command = ""
export.plugin_usage = '用于操作群相关管理。'
export.default_status = True  # 插件默认开关
export.ignore = True  # 插件管理器忽略此插件

config = baseconfig.get('default')


# 零点重置签到数
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    bot_id_list = get_bots()
    for bot_id, bot in bot_id_list.items():
        group_list = await source.sign_reset(int(bot_id))
        count_success = 0
        count_failed = 0
        count_closed = 0
        count_all = len(group_list)
        time_start = time.time()
        for group_id in group_list:
            goodnight_status = await source.get_goodnight_status(int(bot_id), group_id)
            if goodnight_status:
                try:
                    msg = await source.get_goodnight_text(bot_id, group_id)
                    await bot.send_group_msg(group_id=group_id, message=msg)
                    await asyncio.sleep(random.uniform(0.3, 0.5))
                    count_success += 1
                except Exception:
                    log = f'Bot({bot.self_id}) | （{group_id}）群被禁言了，无法发送晚安……'
                    logger.warning(log)
                    count_failed += 1
            else:
                count_closed += 1

        # 获取owner
        time_end = time.time()
        time_use = round(time_end-time_start, 2)
        owner_id = await source.get_bot_owner(bot_id)
        if owner_id is not None:
            msg = f"发送晚安完毕，共发送 {count_all} 个群\n发送成功 {count_success} 个\n发送失败 {count_failed} 个\n关闭通知 {count_closed}个\n用时 {time_use} 秒"
            await bot.send_private_msg(user_id=owner_id, message=msg)


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
didi_admin = on_regex(pattern=r"^滴滴 ", permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=5, block=True)
# 管理员帮助
group_admin_help = on_regex(pattern=r"^管理员帮助$", permission=GROUP, priority=2, block=True)
# 打开关闭进群通知
welcome_status_regex = r"^((打开)|(关闭)) 进群通知$"
welcome_status = on_regex(pattern=welcome_status_regex,
                          permission=OWNER | GROUP_OWNER | GROUP_ADMIN,
                          priority=2,
                          block=True)
# 更改进群通知内容
welcome_text = on_regex(pattern="^进群通知 ", permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)
# 打开关闭离群通知
someoneleft_status_regex = r"^((打开)|(关闭)) 离群通知$"
someoneleft_status = on_regex(pattern=someoneleft_status_regex,
                              permission=OWNER | GROUP_OWNER | GROUP_ADMIN,
                              priority=2,
                              block=True)

# 更改离群通知内容
someoneleft_text = on_regex(pattern="^离群通知 ", permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)
# 打开关闭晚安通知
goodnight_status_regex = r"^((打开)|(关闭)) 晚安通知$"
goodnight_status = on_regex(pattern=goodnight_status_regex,
                            permission=OWNER | GROUP_OWNER | GROUP_ADMIN,
                            priority=2,
                            block=True)
# 更改晚安通知内容
goodnight_text = on_regex(pattern="^晚安通知 ", permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)


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
    nickname = await get_nickname(bot_id)
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
    # 判断欢迎语
    msg = None
    welcome_status = await source.get_welcome_status(bot_id, group_id)
    if welcome_status:
        msg = await source.get_welcome_text(bot_id, group_id)
    await someone_in_group.finish(msg)


@someone_left.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    '''
    群成员减少事件
    '''
    bot_id = int(bot.self_id)
    user_id = event.user_id
    group_id = event.group_id
    # user_name = await source.get_user_name(bot_id, user_id, group_id)
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
        await someone_left.finish()

    # 查看群是否开启机器人
    status = await source.check_robot_status(bot_id, group_id)
    if status is None or status is False:
        await someone_left.finish()

    # 判断开关
    msg = None
    someoneleft_status = await source.get_someoneleft_status(bot_id, group_id)
    if someoneleft_status:
        msg = await source.get_someoneleft_text(bot_id, group_id)

    await someone_left.finish()


@robotchange.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    设置机器人状态
    '''
    bot_id = int(bot.self_id)
    nickname = await get_nickname(bot_id)
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
    nickname = await get_nickname(bot_id)
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

    get_msg = event.get_message()
    get_msg[0] = source.handle_didi_message(get_msg[0])
    msg_0 = MessageSegment.text(f"收到群 {group_name}({group_id}) 内 {user_name}({user_id}) 的滴滴消息：\n\n")
    get_msg.insert(0, msg_0)
    await bot.send_private_msg(user_id=owner, message=get_msg)
    reply = "消息已发送给管理员了……"
    await didi_admin.finish(reply)


@group_admin_help.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''管理员帮助'''
    pagename = "group_admin_help.html"
    img = await get_html_screenshots(pagename)
    msg = MessageSegment.image(img)

    log = f"Bot({bot.self_id}) Group({str(event.group_id)}) | 请求管理员帮助"
    logger.info(log)
    await group_admin_help.finish(msg)


@welcome_status.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''打开关闭进群通知'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    status = (text == "打开 进群通知")
    await source.set_welcome_status(bot_id, group_id, status)
    msg = "进群通知已开启。" if status else "进群通知已关闭。"
    await welcome_status.finish(msg)


@someoneleft_status.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''打开关闭离群通知'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    status = (text == "打开 离群通知")
    await source.set_someoneleft_status(bot_id, group_id, status)
    msg = "离群通知已开启。" if status else "离群通知已关闭。"
    await someoneleft_status.finish(msg)


@goodnight_status.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''打开关闭晚安通知'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    status = (text == "打开 晚安通知")
    await source.set_goodnight_status(bot_id, group_id, status)
    msg = "晚安通知已开启。" if status else "晚安通知已关闭。"
    await someoneleft_status.finish(msg)


@welcome_text.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''修改进群通知内容'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    message = event.get_message()

    command = "进群通知"
    msg_type = "welcome"
    message = source.Message_command_handler(message=message, command=command)
    await source.set_welcome_text(bot_id, group_id, msg_type, message)
    msg = "已设置进群通知内容。"

    await welcome_text.finish(msg)


@someoneleft_text.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''修改离群通知'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    message = event.get_message()

    command = "离群通知"
    msg_type = "someoneleft"
    message = source.Message_command_handler(message=message, command=command)
    await source.set_someoneleft_text(bot_id, group_id, msg_type, message)
    msg = "已设置离群通知内容。"

    await welcome_text.finish(msg)


@goodnight_text.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''修改晚安通知'''
    bot_id = int(bot.self_id)
    group_id = event.group_id
    message = event.get_message()

    command = "晚安通知"
    msg_type = "goodnight"
    message = source.Message_command_handler(message=message, command=command)
    await source.set_goodnight_text(bot_id, group_id, msg_type, message)
    msg = "已设置晚安通知内容。"

    await welcome_text.finish(msg)
