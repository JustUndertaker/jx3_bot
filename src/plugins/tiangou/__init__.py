from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from src.utils.log import logger

from . import data_source as source

export = export()
export.plugin_name = '舔狗日记'
export.plugin_command = "舔狗|日记|舔狗日记"
export.plugin_usage = '返回一条舔狗日记。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件

tiangou_regex = r"(^舔狗$)|(^日记$)|(^舔狗日记$)"
tiangou = on_regex(pattern=tiangou_regex, permission=GROUP, priority=5, block=True)


@tiangou.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    log = f"Bot({bot.self_id}) | 群[{str(group_id)}]请求舔狗日记"
    logger.info(log)
    msg = await source.get_tiangou()
    await tiangou.finish(msg)
