from nonebot import get_driver, on_regex
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import export
from src.utils.browser import close_browser, get_broser
from src.utils.log import logger
from src.utils.scheduler import scheduler
from tortoise import Tortoise

from . import data_source as source

export = export()
export.plugin_name = 'jx3api链接服务'
export.plugin_command = ""
export.plugin_usage = '处理jx3api的ws链接任务'
export.default_status = True  # 插件默认开关
export.ignore = True  # 插件管理器忽略此插件

driver = get_driver()


@driver.on_startup
async def _():
    '''
    初始化链接ws
    '''
    log = 'jx3_api > 开始连接ws.'
    logger.info(log)
    source.init()


@driver.on_shutdown
async def _():
    '''shut_down时关闭链接'''
    log = 'jx3_bot进程关闭，正在清理……'
    logger.info(log)
    log = '关闭无头浏览器'
    logger.info(log)
    browser = get_broser()
    if browser is not None:
        await close_browser()
    log = '关闭数据库'
    logger.info(log)
    await Tortoise.close_connections()
    log = 'jx3_api > 关闭ws链接。'
    logger.info(log)
    ws_connect = source.get_ws_connect()
    await ws_connect.close()


# 查看ws链接状态
ws_check = on_regex(pattern=r"^查看链接$", permission=SUPERUSER, priority=2, block=True)


@ws_check.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    查询ws链接状态
    '''
    ws_connect = source.get_ws_connect()
    if ws_connect.closed:
        msg = 'jx3_api > 当前未链接。'
    else:
        msg = 'jx3_api > 当前链接正常。'
    await ws_check.finish(msg)

# 查看ws链接状态
ws_close = on_regex(pattern=r"^关闭链接$", permission=SUPERUSER, priority=2, block=True)


@ws_close.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    关闭ws链接
    '''
    ws_connect = source.get_ws_connect()
    if ws_connect.closed:
        msg = 'ws已经关闭了，不要重复关闭。'
    else:
        await ws_connect.close()
        msg = 'ws关闭成功！'
    await ws_close.finish(msg)


ws_re_connect = on_regex(pattern=r"^链接服务器$", permission=SUPERUSER, priority=2, block=True)


@ws_re_connect.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''
    重连ws链接
    '''
    ws_connect = source.get_ws_connect()
    if ws_connect.closed:
        await source.on_connect()
        msg = 'jx3_api > 正在重连……'
    else:
        msg = 'jx3_api > 当前已链接，请勿重复链接。'
    await ws_re_connect.finish(msg)


# jx3_api中ws的心跳事件
@scheduler.scheduled_job("interval", seconds=5)
async def _():
    try:
        ws_connect = source.get_ws_connect()
        if ws_connect.closed:
            msg = "检测到jx3_api断开链接！正在重连……"
            logger.debug(msg)
            await source.on_connect()
    except Exception:
        pass
