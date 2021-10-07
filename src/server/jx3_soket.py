import asyncio
import json
from asyncio import AbstractEventLoop
from typing import Optional

import websockets
from nonebot import get_bot, get_bots
from nonebot.message import handle_event
from src.utils.config import config
from src.utils.log import logger
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)
from websockets.legacy.client import WebSocketClientProtocol

from .jx3_event import WS_ECHO, Jx3EventList

ws_echo_list: list[WS_ECHO] = []
'''
消息池，用来维护发送后回复事件
'''

ws_connect: WebSocketClientProtocol
'''
ws全局链接
'''

loop: AbstractEventLoop
'''
事件循环池
'''


def init():
    '''
    初始化
    '''
    global loop
    loop = asyncio.get_event_loop()
    loop.create_task(on_connect())


def get_ws_connect() -> WebSocketClientProtocol:
    global ws_connect
    return ws_connect


async def send_ws_message(msg: dict,
                          echo: int,
                          bot_id: str,
                          user_id: Optional[int] = None,
                          group_id: Optional[int] = None,
                          server: Optional[str] = None,
                          params: Optional[str] = None):
    '''
    使用ws连接发送一条消息
    '''
    global ws_connect
    global ws_echo_list
    ws_echo = WS_ECHO(echo, bot_id, user_id, group_id, server, params)
    ws_echo_list.append(ws_echo)
    if ws_connect.closed:
        log = f"jx3_api > 链接已关闭，代码：{str(ws_connect.close_code)}"
        logger.debug(log)
        loop.create_task(on_connect())
    data = json.dumps(msg)
    await ws_connect.send(data)


async def on_connect():
    global ws_connect
    global loop

    ws_path: str = config.get('jx3-api').get('ws-path')
    max_recon_times: int = config.get('default').get('max-recon-times')

    for count in range(max_recon_times):
        try:
            ws_connect = await websockets.connect(uri=ws_path,
                                                  ping_interval=20,
                                                  ping_timeout=20,
                                                  close_timeout=10)
            logger.info('jx3_api > websockets链接成功！')
            loop.create_task(_task())
            return
        except (ConnectionRefusedError, OSError) as e:
            logger.info(f'jx3_api > [{count}] {e}')
            logger.info(f'jx3_api > [{count}] 尝试向 websockets 服务器建立链接！')
            await asyncio.sleep(1)


async def _task():
    global ws_connect
    global ws_echo_list
    global loop
    try:
        while True:
            data_recv = await ws_connect.recv()
            data = json.loads(data_recv)
            msg_type: int = data['type']
            event = None
            for event_type in Jx3EventList:
                if msg_type == event_type.get_api_type():
                    event = event_type(data)
                    break

            if event is not None:
                if msg_type < 2000:
                    # 请求返回事件，对专门bot返回
                    # 处理发送事件，设置user_id或group_id
                    echo = data['echo']
                    bot_id = None
                    for i, echo_one in enumerate(ws_echo_list):
                        if echo == echo_one.echo:
                            bot_id = echo_one.bot_id
                            event.set_message_type(echo_one)
                            del ws_echo_list[i]
                            break
                    if bot_id is not None:
                        bot = get_bot(self_id=bot_id)
                        await handle_event(bot, event)

                else:
                    # 服务器推送，对所有机器人广播事件
                    log = _get_recv_log(data)
                    logger.debug(log)
                    bots = get_bots()
                    for _, one_bot in bots.items():
                        await handle_event(one_bot, event)

    except (ConnectionClosed, ConnectionClosedError, ConnectionClosedOK) as e:
        ws_connect = None
        if e.code != 1000:
            logger.error('jx3_api > 链接已断开！')
            loop.create_task(on_connect())
        else:
            logger.error('jx3_api > 链接被关闭！')
        logger.error(e)


def _get_recv_log(data: dict) -> str:
    '''
    返回服务器推送日志
    '''
    recv_type = data.get('type')
    recv_data: dict = data.get('data')
    if recv_type == 2001:
        server = recv_data.get('server')
        _stauts = recv_data.get('stauts')
        if _stauts == 1:
            status = "已开服"
        else:
            status = "已维护"
        log = f"开服推送事件：[{server}]状态-{status}"
    elif recv_type == 2002:
        news_type = recv_data.get('type')
        news_tittle = recv_data.get('tittle')
        log = f"[{news_type}]事件：{news_tittle}"
    elif recv_type == 2003:
        server = recv_data.get('server')
        name = recv_data.get('name')
        serendipity = recv_data.get('serendipity')
        log = f"奇遇推送事件：[{server}]的[{name}]抱走了奇遇：{serendipity}"
    return log
