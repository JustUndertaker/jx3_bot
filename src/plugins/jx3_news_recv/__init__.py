import asyncio
import random

from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import export, on
from src.utils.jx3_event import NewsRecvEvent
from utils.utils import GroupList_Async

from . import data_source as source

export = export()
export.plugin_name = '新闻推送'
export.plugin_command = "无"
export.plugin_usage = '推送官方新闻。'
export.default_status = True  # 插件默认开关
export.ignore = False  # 插件管理器忽略此插件


news_recv = on(type="news_recv", priority=5, block=True)  # 新闻推送


@news_recv.handle()
async def _(bot: Bot, event: NewsRecvEvent):
    '''
    新闻推送事件
    '''
    bot_id = int(bot.self_id)
    news_type = event.news_type
    news_tittle = event.news_tittle
    news_url = event.news_url
    news_date = event.news_date

    msg = f"[{news_type}]来惹\n标题：{news_tittle}\n链接：{news_url}\n日期：{news_date}"
    group_list = await bot.get_group_list()
    async for group_id in GroupList_Async(group_list):
        status = await source.get_robot_status(bot_id, group_id)
        if status:
            try:
                await bot.send_group_msg(group_id=group_id, message=msg)
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await news_recv.finish()
