from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.utils.log import logger

from . import data_source as source

export = export()
export.plugin_name = '签到系统'
export.plugin_command = "签到"
export.plugin_usage = '普普通通的签到系统。'
export.default_status = True  # 插件默认开关
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
    msg_req = await source.get_sign_in(bot_id, user_id, group_id, user_name)
    msg = MessageSegment.at(user_id)+msg_req
    await sign.finish(msg)
