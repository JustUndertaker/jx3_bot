from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot import on_regex, get_driver
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from utils.utils import scheduler, get_bot
import random

from .data_source import get_sign_in, reset, update_info
from .config import RANDOM_SAID_SCHEDULER
from utils.log import logger
from nonebot.plugin import export

export = export()
export.plugin_name = '签到'
export.plugin_usage = '普普通通的签到系统，每天0点重置\n命令：签到'


driver = get_driver()


# 链接bot时处理，自动注册所有群信息
@driver.on_bot_connect
async def _(bot: Bot):
    group_list = await bot.get_group_list()
    log = f'链接bot成功，加载{len(group_list)}个群，正在注册群帮助信息。'
    logger.debug(log)
    for group in group_list:
        group_id = group['group_id']
        member_list = await bot.get_group_member_list(group_id=group_id)
        await update_info(group_id, member_list)
    log = '所有群信息注册完毕。'
    logger.debug(log)


sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    user_name = event.sender.card
    if user_name == '':
        user_name = event.sender.nickname
    group_id = event.group_id

    log = f'{user_name}（{user_id}，{group_id}）请求：签到'
    logger.info(log)
    msg = await get_sign_in(user_id, group_id, user_name)
    await sign.finish(msg)

update = on_regex(r"^更新$", permission=SUPERUSER, priority=5, block=True)


@update.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    bot = get_bot()
    group_id = event.group_id
    member_list = await bot.get_group_member_list(group_id=group_id)
    msg = await update_info(group_id, member_list)
    log = f'（{event.group_id}）管理员更新信息'
    logger.info(log)
    await update.finish(msg)


# 定时任务
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    group_list = await reset()
    bot = get_bot()
    for group_id in group_list:
        try:
            msg = random.choice(RANDOM_SAID_SCHEDULER)
            await bot.send_group_msg(group_id=group_id, message=msg)
        except Exception:
            log = f'（{group_id}）群被禁言了，无法发送晚安……'
            logger.warning(log)
