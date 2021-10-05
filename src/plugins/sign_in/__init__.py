import asyncio
import random
import time

from nonebot import get_bots, on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.utils.log import logger
from src.utils.scheduler import scheduler
from src.utils.utils import nickname

from .data_source import get_bot_owner, get_sign_in, reset

export = export()
export.plugin_name = '签到系统'
export.plugin_usage = '普普通通的签到系统。'
export.ignore = False  # 插件管理器忽略此插件

sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    bot_id = int(bot.self_id)
    user_id = event.user_id
    user_name = event.sender.nickname if event.sender.card == "" else event.sender.card
    group_id = event.group_id

    log = f'Bot({bot.self_id}) | {user_name}（{user_id}，{group_id}）请求：签到'
    logger.info(log)
    msg_req = await get_sign_in(bot_id, user_id, group_id, user_name)
    msg = MessageSegment.at(user_id)+msg_req
    await sign.finish(msg)


# 定时任务
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    bot_id_list = get_bots()
    for bot_id, bot in bot_id_list.items():
        group_list = await reset(int(bot_id))
        count_success = 0
        count_failed = 0
        count_all = len(group_list)
        time_start = time.time()
        for group_id in group_list:
            try:
                msg = f"{nickname}要去睡觉了，大家晚安……"
                await bot.send_group_msg(group_id=group_id, message=msg)
                await asyncio.sleep(random.uniform(0.3, 0.5))
                count_success += 1
            except Exception:
                log = f'Bot({bot.self_id}) | （{group_id}）群被禁言了，无法发送晚安……'
                logger.warning(log)
                count_failed += 1
        # 获取owner
        time_end = time.time()
        time_use = round(time_end-time_start, 2)
        owner_id = await get_bot_owner(bot_id)
        if owner_id is not None:
            msg = f"发送晚安完毕，共发送 {count_all} 个群\n成功 {count_success} 个\n失败 {count_failed} 个\n用时 {time_use} 秒"
            await bot.send_private_msg(user_id=owner_id, message=msg)
