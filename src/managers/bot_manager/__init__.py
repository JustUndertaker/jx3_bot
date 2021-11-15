import asyncio
import random
import time
from datetime import datetime

from nonebot import get_bots, get_driver, on_regex
from nonebot.adapters.cqhttp import Bot, MessageSegment, PrivateMessageEvent
from nonebot.adapters.cqhttp.permission import PRIVATE_FRIEND
from nonebot.permission import SUPERUSER
from nonebot.plugin import export
from src.utils.browser import get_html_screenshots
from src.utils.config import config
from src.utils.log import logger
from src.utils.scheduler import scheduler
from src.utils.utils import OWNER

from . import data_source as source

export = export()
export.plugin_name = 'bot管理插件'
export.plugin_command = ""
export.plugin_usage = '用于bot的管理'
export.default_status = True  # 插件默认开关
export.ignore = True  # 插件管理器忽略此插件

driver = get_driver()

outtime: int = config.get('default').get('bot-outtime')


@driver.on_bot_connect
async def _(bot: Bot):
    '''
    链接bot
    '''
    bot_id = int(bot.self_id)
    log = f'连接到bot（{bot.self_id}），正在注册信息'
    logger.info(log)
    await source.bot_connect(bot_id)
    log = f'bot（{bot.self_id}）信息注册完毕'
    logger.info(log)


@driver.on_bot_disconnect
async def _(bot: Bot):
    '''
    机器人断开链接
    '''
    bot_id = int(bot.self_id)
    log = f'检测到bot（{bot.self_id}）断开链接.'
    logger.info(log)
    await source.bot_disconnect(bot_id)


# 定时清理离线超过时间的Bot
@scheduler.scheduled_job("cron", hour=23, minute=59)
async def _():
    log = '正在清理离线bot'
    logger.info(log)
    outtime = config.get('default').get('bot-outtime')
    count = await source.clean_bot(outtime)
    log = f'清理完毕，本次共清理 {count} 个机器人数据'
    logger.info(log)


# 设置管理员
set_owner = on_regex(pattern=r"^设置管理员$", permission=PRIVATE_FRIEND, priority=2, block=True)
# 清除管理员
clean_owner = on_regex(pattern=r"^清除管理员$", permission=PRIVATE_FRIEND, priority=2, block=True)
# 管理员广播
borodcast_all = on_regex(pattern=r"^全体广播 ", permission=OWNER, priority=2, block=True)
borodcast = on_regex(pattern=r"^广播 [0-9]+ ", permission=OWNER, priority=2, block=True)
# 查看所有连接机器人
server_list = on_regex(pattern=r"^服务器列表$", permission=SUPERUSER, priority=2, block=True)
# 授权高级功能
open_permission = on_regex(pattern=r"^授权 [0-9]+$", permission=SUPERUSER, priority=2, block=True)
close_permission = on_regex(pattern=r"^取消授权 [0-9]+$", permission=SUPERUSER, priority=2, block=True)
# 手动清理离线机器人
clean_outline_bot = on_regex(pattern=r"(^清理所有离线$)|(^清理离线 [0-9]+$)", permission=SUPERUSER, priority=2, block=True)
# 管理员更新数据库
update_database = on_regex(pattern=r"^清理数据$", permission=SUPERUSER, priority=2, block=True)


@set_owner.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''私聊设置管理员'''
    bot_id = int(bot.self_id)
    owner_id = event.user_id
    nickname = event.sender.nickname
    flag = await source.set_bot_owner(bot_id, owner_id)
    if flag is None:
        msg = "设置失败，机器人记录不存在。"
    elif flag:
        msg = f'设置成功，当前管理员为：{nickname}（{owner_id}）'
    else:
        msg = "设置失败，该机器人已有管理员。\n如需要更换管理员，请管理员账号输入：清除管理员"
    await set_owner.finish(msg)


@clean_owner.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''清除管理员'''
    bot_id = int(bot.self_id)
    owner_id = event.user_id
    flag = await source.clean_bot_owner(bot_id, owner_id)
    if flag is None:
        msg = "没有什么好清除的了。"
    elif flag:
        msg = "清除成功，可以重新设置管理员了。"
    else:
        msg = "清除失败惹，你不是管理员。"
    await clean_owner.finish(msg)


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


@server_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    查看所有链接机器人
    '''
    data = await source.get_all_bot()
    for one_data in data:
        if one_data['owner_id'] is None:
            one_data['owner_id'] = "无"
        last_sign: datetime = one_data['last_sign']
        one_data['last_sign'] = last_sign.strftime("%Y-%m-%d %H:%M:%S")
        if one_data['last_left'] is None:
            one_data['last_left'] = "无记录"
        else:
            last_left: datetime = one_data['last_left']
            one_data['last_left'] = last_left.strftime("%Y-%m-%d %H:%M:%S")
    alldata = {}
    alldata['data'] = data
    alldata['robot_nums'] = len(data)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alldata['time'] = now_time
    pagename = "robot.html"
    img = await get_html_screenshots(pagename=pagename, data=alldata)
    msg = MessageSegment.image(img)
    await server_list.finish(msg)


@open_permission.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    私聊授权高级功能
    '''
    bot_id = int(event.get_plaintext().split(" ")[-1])
    req = await source.set_permission(bot_id, True)
    if req:
        msg = f"授权成功，机器人[{bot_id}]已开启高级功能。"
    else:
        msg = f"授权失败，未找到机器人[{bot_id}]。"
    await open_permission.finish(msg)


@close_permission.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    私聊取消高级功能
    '''
    bot_id = int(event.get_plaintext().split(" ")[-1])
    req = await source.set_permission(bot_id, False)
    if req:
        msg = f"机器人[{bot_id}]已关闭高级功能。"
    else:
        msg = f"失败，未找到机器人[{bot_id}]。"
    await close_permission.finish(msg)


@clean_outline_bot.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    私聊清理离线bot
    '''
    text_list = event.get_plaintext().split(" ")
    if len(text_list) == 1:
        outtime = 0
    else:
        outtime = int(text_list[-1])
    log = f"管理员清理机器人，参数：{outtime}"
    logger.info(log)
    count = await source.clean_bot(outtime)
    msg = f"清理完毕，共清理 {str(count)} 个机器人。"
    await clean_outline_bot.finish(msg)


@update_database.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    超级用户更新数据库
    '''
    msg = "开始清理数据库"
    await update_database.send(msg)

    msg_dict = {}
    botdict = get_bots()
    for id, one_bot in botdict.items():
        bot_id = int(id)
        count = 0
        group_list = [x['group_id'] for x in await one_bot.get_group_list()]
        data_group_list = await source.get_bot_group_list(bot_id)
        for one_group in data_group_list:
            if one_group not in group_list:
                # 数据不在群列表中
                await source.clean_one_group(bot_id, one_group)
                # 记录
                count += 1

        msg_dict[id] = count

    msg = "数据库清理完毕……\n"
    for id, count in msg_dict.items():
        msg += f"bot[{id}] 共清理群数据 {count} 个.\n"

    await update_database.finish(msg)
