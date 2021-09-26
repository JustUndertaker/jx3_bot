import asyncio
import random

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.utils.log import logger
from src.utils.scheduler import scheduler
from src.utils.utils import get_bot, nickname

from .data_source import get_sign_in, reset

export = export()
export.plugin_name = '签到系统'
export.plugin_usage = '普普通通的签到系统。'
export.ignore = False  # 插件管理器忽略此插件

sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_id = event.user_id
    user_name = event.sender.nickname if event.sender.card == "" else event.sender.card
    group_id = event.group_id

    log = f'{user_name}（{user_id}，{group_id}）请求：签到'
    logger.info(log)
    msg_req = await get_sign_in(user_id, group_id, user_name)
    msg = MessageSegment.at(user_id)+msg_req
    await sign.finish(msg)


# 定时任务
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    group_list = await reset()
    bot = get_bot()
    for group_id in group_list:
        try:
            msg = f"{nickname}要去睡觉了，大家晚安……"
            await bot.send_group_msg(group_id=group_id, message=msg)
            await asyncio.sleep(random.uniform(0.3, 0.5))
        except Exception:
            log = f'（{group_id}）群被禁言了，无法发送晚安……'
            logger.warning(log)
