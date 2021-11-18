import random

from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export

from . import data_source as source

export = export()
export.plugin_name = '自动插话'
export.plugin_command = "无"
export.plugin_usage = '让机器人自动插话。'
export.default_status = False  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件


message = on_message(permission=GROUP, priority=99, block=True)


@message.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''
    处理自动插话
    '''
    # 是否随机插话
    bot_id = int(bot.self_id)
    num = random.randrange(100)
    active = await source.get_active(bot_id, event.group_id)
    if num > active:
        await message.finish()

    # 获取一条骚话
    text = await source.get_saohua()
    num = random.randrange(100)
    if num < 20:
        # 是否转换语音
        voice_str = await source.get_voice(text)
        if voice_str is not None:
            msg = MessageSegment.record(voice_str)
            await message.finish(msg)

    msg = MessageSegment.text(text)
    await message.finish(msg)
