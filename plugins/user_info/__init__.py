from nonebot.adapters.cqhttp import GROUP
from nonebot.plugin import export, on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.typing import T_State

from modules.user_info import UserInfo

export = export()
export.plugin_name = '用户信息'
export.plugin_usage = '查看当前我的信息\n命令：我的'

user = on_regex(r"^我的$", permission=GROUP, priority=5, block=True)


@user.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    group_id = event.group_id
    text = await UserInfo.user_display(user_id, group_id)
    await user.finish(text)
