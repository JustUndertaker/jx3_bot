from nonebot import on_regex, get_driver
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment, GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.message import run_preprocessor
from nonebot.plugin import Matcher
from nonebot.permission import SUPERUSER
from utils.log import logger
from nonebot.typing import T_State
import os
from .model import manager_init
from nonebot.exception import IgnoredException
from utils.browser import get_html_screenshots
from .data_source import (
    check_plugin_status,
    plugin_init,
    change_plugin_status,
    check_group_init,
    get_meau_data,
)


# 获取本模块名
_, self_module = os.path.split(os.path.split(__file__)[0])

# ==============插件管理器注册==============
driver = get_driver()

# 启动处理，生成插件管理模块
driver.on_startup(manager_init)


# 链接bot时处理，自动为所有群注册插件
@driver.on_bot_connect
async def _(bot: Bot):
    group_list = await bot.get_group_list()
    log = '开始自动为所有群注册插件信息……'
    logger.debug(log)
    for group in group_list:
        group_id = group['group_id']
        await plugin_init(group_id)
    log = '插件信息注册完毕。'
    logger.debug(log)


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

    # 判断是否注册
    is_init = await check_group_init(group_id)
    if is_init is None or module_name == self_module:
        log = '此插件不归管理器管理，跳过。'
        logger.debug(log)
        return

    # 管理器管理函数
    status = await check_plugin_status(module_name, group_id)

    if status is False:
        reason = f'[{module_name}]插件未开启'
        log = f'事件被阻断：{reason}'
        logger.debug(log)
        raise IgnoredException(reason)


# =================================管理员手动更新==========================
update = on_regex(r"^更新$", permission=SUPERUSER, priority=2, block=True)


@update.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    管理员手动更新群信息
    '''
    # 群id
    group_id = event.group_id
    # 注册
    log = f'超级用户手动注册群插件：{group_id}'
    logger.info(log)
    await plugin_init(group_id)

changeregex = r'^设置 [\u4E00-\u9FA5A-Za-z0-9_]+ [开|关]$'
change = on_regex(changeregex, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=True)


# =================================功能开关===============================
@change.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    text = event.get_plaintext()
    try:
        plugin_name, status = _get_change_params(text)
        log = f'（{group_id}）群尝试设置插件[{plugin_name}]的状态：[{status}]。'
        logger.info(log)
        msg = await change_plugin_status(plugin_name, group_id, status)
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
    try:
        plugin_name = text_list[1]
        _status = text_list[2]
        if _status == '开':
            status = True
        elif _status == '关':
            status = False
        else:
            raise Exception
    except Exception:
        raise Exception
    return plugin_name, status


# ===============插件菜单===============
meauregex = r'(^菜单$)|(^功能$)'
meau = on_regex(meauregex, permission=GROUP, priority=2, block=True)


@meau.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    显示功能开关状态
    '''
    self_id = event.self_id
    group_id = event.group_id
    log = f'{event.sender.nickname}（{event.user_id}，{event.group_id}）请求功能菜单。'
    logger.info(log)
    data = await get_meau_data(self_id, group_id)
    pagename = "meau.html"
    img = await get_html_screenshots(pagename, data)
    msg = MessageSegment.image(img)
    await meau.finish(msg)
