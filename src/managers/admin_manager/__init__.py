import asyncio
import random
import re
import time
from datetime import datetime

from nonebot import on_message, on_notice, on_regex, on_request
from nonebot.adapters.cqhttp import (Bot, FriendAddNoticeEvent,
                                     FriendRequestEvent, GroupRequestEvent,
                                     MessageSegment, PrivateMessageEvent)
from nonebot.plugin import export
from nonebot.typing import T_State
from src.utils.browser import get_html_screenshots
from src.utils.config import config as baseconfig
from src.utils.log import logger
from src.utils.utils import OWNER, get_nickname

from . import data_source as source

export = export()
export.plugin_name = '超级用户管理'
export.plugin_usage = '用于超级用户私聊机器人管理指令。'
export.plugin_command = ""
export.default_status = True  # 插件默认开关
export.ignore = True  # 插件管理器忽略此插件

config = baseconfig.get('default')

# 添加好友通知事件
check_firend_add = ['notice.friend_add']
someone_add_me = on_notice(rule=source.check_event(check_firend_add), priority=3, block=True)
# 请求好友事件
check_friend_add = ['request.friend']
friend_add = on_request(rule=source.check_event(check_friend_add), priority=3, block=True)
# 群邀请事件
check_group_add = ['request.group.invite']
group_add = on_request(rule=source.check_event(check_group_add), priority=3, block=True)

# 查看运行状态
group_list_event = ['message.private.friend', 'message.private.group']
get_group_list = on_regex(pattern=r"(^状态$)|(^运行状态$)",
                          rule=source.check_event(group_list_event),
                          permission=OWNER,
                          priority=2,
                          block=True)

# 打开/关闭群机器人
group_status_regex = r"^(打开|关闭) [0-9]+$"
set_group_status = on_regex(pattern=group_status_regex,
                            rule=source.check_event(group_list_event),
                            permission=OWNER,
                            priority=2,
                            block=True)

# 打开/关闭所有机器人
change_all_regex = r"^(打开|关闭)所有$"
change_all = on_regex(pattern=change_all_regex,
                      rule=source.check_event(group_list_event),
                      permission=OWNER,
                      priority=2,
                      block=True)

# 私聊消息聊天
chat_event = ['message.private.friend', 'message.private.group']
chat = on_message(rule=source.check_event(chat_event), priority=9, block=True)

# 退群指令
set_group_leave_regex = r"^退群 [0-9]+$"
set_group_leave = on_regex(pattern=set_group_leave_regex,
                           rule=source.check_event(chat_event),
                           permission=OWNER,
                           priority=2,
                           block=True)

# 好友列表
get_friend_regex = r"^好友列表$"
get_friend = on_regex(pattern=get_friend_regex,
                      rule=source.check_event(chat_event),
                      permission=OWNER,
                      priority=2,
                      block=True)

# 删除好友
detele_friend_regex = r"^删除好友 [0-9]+$"
detele_friend = on_regex(pattern=detele_friend_regex,
                         rule=source.check_event(chat_event),
                         permission=OWNER,
                         priority=2,
                         block=True)

# 帮助信息
owner_help = on_regex(pattern=r"^帮助$", permission=OWNER, priority=2, block=True)
# 管理员广播
borodcast_all = on_regex(pattern=r"^全体广播 ", permission=OWNER, priority=2, block=True)
borodcast = on_regex(pattern=r"^广播 [0-9]+ ", permission=OWNER, priority=2, block=True)

# 设置昵称
set_nickname = on_regex(pattern=r"^设置昵称 [\u4E00-\u9FA5A-Za-z0-9_]+$", permission=OWNER, priority=2, block=True)

# 增加token
add_token = on_regex(pattern=r"^^token [(A-Za-z0-9)|(:)|(=)]+$", permission=OWNER, priority=2, block=True)
# 查看token
check_token = on_regex(pattern=r"^token$", permission=OWNER, priority=2, block=True)


@someone_add_me.handle()
async def _(bot: Bot, event: FriendAddNoticeEvent):
    '''添加好友'''
    bot_id = int(bot.self_id)
    user_id = event.user_id
    user_info = await bot.get_stranger_info(user_id=user_id, no_cache=True)
    user_name = user_info['nickname']
    msg = f"我添加了好友[{user_name}]({user_id})"
    owner_id = await source.get_bot_owner(bot_id)
    log = f"Bot({bot.self_id}) | 添加了好友[{user_name}]({user_id})"
    logger.info(log)
    if owner_id is not None:
        await bot.send_private_msg(user_id=owner_id, message=msg)
    await someone_add_me.finish()


@friend_add.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    '''加好友请求事件'''
    access_firend = config.get('access-firend')
    if access_firend:
        await event.approve(bot)
    await friend_add.finish()


@group_add.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    '''加群请求事件'''
    access_group = config.get('access-group')
    if access_group:
        await event.approve(bot)
    await group_add.finish()


@get_group_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''管理员获取机器人状态'''
    bot_id = int(bot.self_id)
    nickname = await get_nickname(bot_id)
    data = {}
    groups = await source.get_all_data(bot_id)
    group_nums = len(groups)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['time'] = time_now
    data['groups'] = groups
    data['group_nums'] = group_nums
    data['nickname'] = nickname

    pagename = "status.html"
    img = await get_html_screenshots(pagename=pagename, data=data)
    msg = MessageSegment.image(img)
    log = f"Bot({bot.self_id}) | 管理员获取运行状态"
    logger.info(log)
    await get_group_list.finish(msg)


@set_group_status.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''管理员私聊打开关闭机器人'''
    bot_id = int(bot.self_id)
    text = event.get_plaintext()
    status, group_id = source.get_text_num(text)
    result = await source.set_robot_status(bot_id, group_id, status)
    if result:
        msg = f"群（{group_id}）状态设置成功！"
    else:
        msg = f"未找到群（{group_id}），设置失败！"

    log = f"Bot({bot.self_id}) | 管理员命令：{msg}"
    logger.info(log)
    await set_group_status.finish(msg)


@change_all.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''管理员私聊打开关闭所有'''
    bot_id = int(bot.self_id)
    text = event.get_plaintext()
    status = (text == "打开所有")
    await source.change_status_all(bot_id, status)
    if status:
        msg = "所有群已打开机器人！"
    else:
        msg = "所有群已关闭机器人！"

    log = f"Bot({bot.self_id}) | 管理员命令：{msg}"
    logger.info(log)
    await change_all.finish(msg)


@chat.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''其他人私聊消息
    自动根据确定API
    '''
    bot_id = int(bot.self_id)
    nickname = await get_nickname(bot_id)
    private_chat = config.get('private-chat')
    if not private_chat:
        await chat.finish()
    # 获得聊天内容
    text = event.get_plaintext()
    name = event.sender.nickname
    log = f'Bot({bot.self_id}) | {name}（{event.user_id}）私聊闲聊：{text}'
    logger.info(log)

    # 使用jx3api访问
    msg = await source.get_reply_jx3(text, nickname)
    if msg is None:
        # 使用青云客访问
        msg = await source.get_reply_qingyunke(text, nickname)
        if msg is None:
            # 访问失败
            log = '接口访问失败，关闭事件。'
            logger.info(log)
            await chat.finish()

    log = f'接口返回：{msg}'
    logger.info(log)
    await chat.finish(msg)


@set_group_leave.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''私聊退群'''
    text = event.get_plaintext()
    bot_id = int(bot.self_id)
    group_id = int(text.split(' ')[-1])
    flag, group_name = await source.leave_group(bot_id, group_id)
    if flag:
        await bot.set_group_leave(group_id=group_id, is_dismiss=True)
        msg = f'成功，已退出群：[{group_name}]({group_id})'
    else:
        msg = f'失败，未找到群：({group_id})。'

    log = f"Bot({bot.self_id}) | 管理员命令：{msg}"
    logger.info(log)
    await set_group_leave.finish(msg)


@get_friend.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''获取好友列表'''
    bot_id = int(bot.self_id)
    nickname = await get_nickname(bot_id)
    self_id = event.self_id
    friend_list = await bot.get_friend_list()
    friends = []
    for friend in friend_list:
        if self_id == friend.get('user_id'):
            continue
        one_friend = {}
        one_friend['user_name'] = friend.get('nickname')
        one_friend['user_id'] = friend.get('user_id')
        friends.append(one_friend)
    data = {}
    data['friends'] = friends
    data['nickname'] = nickname
    data['friend_nums'] = len(friends)
    pagename = "friend.html"
    img = await get_html_screenshots(pagename, data)
    msg = MessageSegment.image(img)

    log = f"Bot({bot.self_id}) | 管理员获取好友列表"
    logger.info(log)
    await get_friend.finish(msg)


@detele_friend.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''私聊删好友'''

    text = event.get_plaintext()
    user_id = int(text.split(' ')[-1])
    friend_list = await bot.get_friend_list()
    flag = False
    user_name = ""
    for friend in friend_list:
        if user_id == friend.get('user_id'):
            flag = True
            user_name = friend.get('nickname')
            break

    if flag:
        try:
            await bot.call_api(api="delete_friend", id=user_id)
            msg = f'成功，删除好友：{user_name}({user_id})。'
        except Exception as e:
            msg = f'删除好友失败：{str(e)}'
    else:
        msg = f'失败，未找到好友：({user_id})。'

    log = f"Bot({bot.self_id}) | 管理员命令：{msg}"
    logger.info(log)
    await detele_friend.finish(msg)


@owner_help.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''管理员私聊帮助'''
    pagename = "owner_help.html"
    img = await get_html_screenshots(pagename)
    msg = MessageSegment.image(img)

    log = f"Bot({bot.self_id}) | 管理员私聊帮助"
    logger.info(log)
    await owner_help.finish(msg)


@borodcast_all.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    管理员广播，全体广播
    '''
    bot_id = int(bot.self_id)
    get_msg = event.get_message()
    get_msg[0], _ = source.handle_borad_message(all=True, one_message=get_msg[0])
    msg_0 = MessageSegment.text('管理员广播消息：\n\n')
    get_msg.insert(0, msg_0)

    group_list = await source.get_bot_group_list(bot_id)
    num = len(group_list)
    time_start = time.time()
    count_success = 0
    count_failed = 0
    for group_id in group_list:
        try:
            await bot.send_group_msg(group_id=group_id, message=get_msg)
            await asyncio.sleep(random.uniform(0.3, 0.5))
            count_success += 1
        except Exception:
            count_failed += 1
    time_end = time.time()
    time_use = round(time_end-time_start, 2)
    msg = f"发送完毕，共发送 {num} 个群\n成功 {count_success} 个\n失败 {count_failed} 个\n用时 {time_use} 秒"
    await borodcast_all.finish(msg)


@borodcast.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    广播某个群
    '''
    bot_id = int(bot.self_id)
    get_msg = event.get_message()
    get_msg[0], group_id = source.handle_borad_message(all=False, one_message=get_msg[0])
    msg_0 = MessageSegment.text('管理员广播消息：\n\n')
    get_msg.insert(0, msg_0)

    robot_status = await source.get_robot_status(bot_id, group_id)
    if robot_status is None:
        msg = f"广播失败，未找到群[{str(group_id)}]。"
        await borodcast.finish(msg)
    elif robot_status is False:
        msg = f"广播失败，机器人在群[{str(group_id)}]处于关闭。"
        await borodcast.finish(msg)
    try:
        await bot.send_group_msg(group_id=group_id, message=get_msg)
        msg = f"广播已发送至群[{str(group_id)}]。"
    except Exception:
        msg = f"广播失败至群[{str(group_id)}]失败，可能被禁言。"
    await borodcast.finish(msg)


@set_nickname.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''设置昵称'''
    bot_id = bot.self_id
    nickname = event.get_plaintext().split(" ")[-1]
    await source.set_bot_nickname(bot_id, nickname)
    msg = f"设置成功，机器人目前昵称为：{nickname}"
    await set_nickname.finish(msg)


@add_token.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''增加一条token'''
    bot_id = int(bot.self_id)
    token = event.get_plaintext().split(" ")[-1]
    # 验证token
    alive, req_msg = await source.check_token(ticket=token)
    if not alive:
        msg = f"添加token失败，{req_msg}。"
        await add_token.finish(msg)

    flag = await source.add_token(bot_id, token)
    if flag:
        msg = "添加token成功了！"
    else:
        msg = "添加token失败，token已存在！"

    await add_token.finish(msg)


@check_token.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    '''查看token'''
    bot_id = int(bot.self_id)
    token_list = await source.get_token(bot_id)
    state['token_list'] = token_list
    state['got'] = True

    data = {}
    data['data'] = token_list
    data['token_nums'] = len(token_list)
    pagename = "token_info.html"
    img = await get_html_screenshots(pagename, data)
    msg = MessageSegment.image(img)

    await check_token.send(msg)


@check_token.got(key="got")
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    '''等待后续命令'''
    bot_id = int(bot.self_id)
    token_list = state['token_list']

    text = event.get_plaintext()
    match = re.match(pattern=r"^退出$", string=text)
    if match:
        msg = "退出token管理。"
        await check_token.finish(msg)

    match = re.match(pattern=r"^删除 [0-9]+$", string=text)
    if not match:
        msg = "输入“删除 [序号]”删除token，输入“退出”结束管理"
        await check_token.reject(msg)

    count = int(text.split(' ')[-1])
    try:
        token = token_list[count-1]['token']
    except Exception:
        msg = "输入序号有误!请重新输入。"
        await check_token.reject(msg)

    flag = await source.remove_token(bot_id, token)
    if flag:
        msg = "已删除该token！退出管理。"
    else:
        msg = "删除token失败！退出管理。"
    await check_token.finish(msg)
