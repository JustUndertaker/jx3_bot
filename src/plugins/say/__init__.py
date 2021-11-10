from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from nonebot.rule import to_me
from src.utils.log import logger

from .data_source import get_voice

export = export()
export.plugin_name = '语音说'
export.plugin_command = "@机器人+说XXX"
export.plugin_usage = '让机器人说话。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件

say = on_regex(pattern=r"^说", rule=to_me(), permission=GROUP, priority=5, block=True)


@say.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    _text = event.get_plaintext()
    loc = _text.find("说")
    text = _text[loc+1:]
    log = f"Bot({bot.self_id}) | 群[{str(group_id)}]请求说话：{text}"
    logger.info(log)
    voice_str = await get_voice(text)
    if voice_str is not None:
        msg = MessageSegment.record(voice_str)
        await say.finish(msg)
    else:
        await say.finish()
