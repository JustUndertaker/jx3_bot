import os

from nonebot import get_driver, on_regex
from nonebot.adapters.cqhttp import (GROUP_ADMIN, GROUP_OWNER, Bot,
                                     GroupMessageEvent, MessageSegment)
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.plugin import Matcher
from nonebot.typing import T_State
from src.utils.browser import get_html_screenshots
from src.utils.log import logger
from src.utils.utils import OWNER, get_nickname

from . import data_source as source
from .model import manager_init

# 获取本模块名
_, self_module = os.path.split(os.path.split(__file__)[0])

# ==============插件管理器注册==============
driver = get_driver()

# 启动处理，生成插件管理模块
driver.on_startup(manager_init)


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    插件管理预处理函数，只处理群消息
    '''
    # 跳过不是群消息的事件
    event_type = event.get_event_name()
    if event_type != "message.group.normal":
        return

    # 获取群号id
    group_id = event.group_id
    # 获取插件模块名
    module_name = matcher.plugin_name
    bot_id = int(bot.self_id)

    # 判断是否注册
    is_init = await source.check_group_init(bot_id, group_id, module_name)
    if is_init is False or module_name == self_module:
        log = f'Bot({bot.self_id}) | 此插件不归管理器管理，跳过。'
        logger.debug(log)
        return

    # 管理器管理函数
    status = await source.check_plugin_status(bot_id, module_name, group_id)

    if status is False:
        reason = f'[{module_name}]插件未开启'
        log = f'Bot({bot.self_id}) | 事件被阻断：{reason}'
        logger.debug(log)
        raise IgnoredException(reason)


# =================================管理员手动更新==========================
update = on_regex(r"^更新信息$", permission=OWNER, priority=2, block=True)


@update.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    管理员手动更新群信息
    '''
    bot_id = int(bot.self_id)
    # 群id
    group_id = event.group_id
    # 注册
    log = f'Bot({bot.self_id}) | 管理员手动注册群插件：{group_id}'
    logger.info(log)
    await source.plugin_init(bot_id, group_id)

changeregex = r'^(打开|关闭) [\u4E00-\u9FA5A-Za-z0-9_]+$'
change = on_regex(changeregex, permission=OWNER | GROUP_OWNER | GROUP_ADMIN, priority=3, block=True)


# =================================功能开关===============================
@change.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    bot_id = int(bot.self_id)
    group_id = event.group_id
    text = event.get_plaintext()
    try:
        plugin_name, status = _get_change_params(text)
        log = f'Bot({bot.self_id}) | （{group_id}）群尝试设置插件[{plugin_name}]的状态：[{status}]。'
        logger.info(log)
        msg = await source.change_plugin_status(bot_id, plugin_name, group_id, status)
        log = f'插件[{plugin_name}]状态设置成功。'
        logger.info(log)
    except Exception:
        log = f'插件[{plugin_name}]状态设置失败。'
        logger.info(log)
        msg = MessageSegment.text('参数正确吗？检查一下。')

    await change.finish(msg)


def _get_change_params(text: str) -> tuple[str, bool]:
    '''
    :说明
        从原始消息中解析出插件名和开关状态

    :参数
        原始消息

    :返回
        * plugin_name：插件名
        * status：开关状态
    '''
    text_list = text.split(' ')
    plugin_name = text_list[1]
    _status = text_list[0]
    status = (_status == "打开")
    return plugin_name, status


# ===============插件菜单===============
meauregex = r'(^菜单$)|(^功能$)|(^状态$)'
meau = on_regex(meauregex, permission=GROUP, priority=2, block=True)


@meau.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    显示功能开关状态
    '''
    self_id = int(bot.self_id)
    nickname = await get_nickname(self_id)
    group_id = event.group_id
    log = f'Bot({bot.self_id}) | {event.sender.nickname}（{event.user_id}，{event.group_id}）请求功能菜单。'
    logger.info(log)
    data = await source.get_meau_data(self_id, group_id, nickname)
    pagename = "meau.html"
    img = await get_html_screenshots(pagename, data)
    msg = MessageSegment.image(img)
    await meau.finish(msg)


help_info = on_regex(pattern=r"^帮助$", permission=GROUP, priority=2, block=True)


@help_info.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''帮助info'''
    pagename = "search_help.html"
    img = await get_html_screenshots(pagename)
    msg = MessageSegment.image(img)
    log = f"Bot({bot.self_id}) | 群[{event.group_id}]请求帮助"
    logger.info(log)
    await help_info.finish(msg)
