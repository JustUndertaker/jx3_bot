from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot import on_message
from nonebot.plugin import export
import random
from .data_source import (
    get_active,
    get_saohua,
    get_voice,
)

export = export()
export.plugin_name = '自动插话'
export.plugin_usage = '让机器人自动插话。'
export.ignore = False  # 插件管理器忽略此插件


message = on_message(permission=GROUP, priority=99, block=True)


@message.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    处理自动插话
    '''
    # 随机是否插话
    num = random.randrange(100)
    active = await get_active(event.group_id)
    if num > active:
        await message.finish()

    # 获取一条骚话
    text = await get_saohua()
    num = random.randrange(100)
    if num < 20:
        # 转换语音
        voice_str = await get_voice(text)
        if voice_str is not None:
            msg = MessageSegment.record(voice_str)
            await message.finish(msg)

    msg = MessageSegment.text(text)
    await message.finish(msg)
