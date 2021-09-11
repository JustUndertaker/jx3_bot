import asyncio
import json
from asyncio import AbstractEventLoop
from typing import Optional

import websockets
from configs.config import MAX_RECON_TIMES
from nonebot import get_bots
from nonebot.message import handle_event
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)

from utils.log import logger

from .jx3_event import WS_ECHO, Jx3EventList

ws_echo_list: list[WS_ECHO] = []
'''
消息池，用来维护发送后回复事件
'''

ws_connect = None
'''
ws全局链接
'''


async def send_ws_message(msg: dict, echo: int, user_id: Optional[int] = None, group_id: Optional[int] = None):
    '''
    使用ws连接发送一条消息
    '''
    global ws_connect
    global ws_echo_list
    ws_echo = WS_ECHO(echo, user_id, group_id)
    ws_echo_list.append(ws_echo)
    if ws_connect is not None:
        data = json.dumps(msg)
        await ws_connect.send(data)


async def on_connect(loop: AbstractEventLoop):
    count = 0
    global ws_connect

    while True:
        try:
            ws_connect = await websockets.connect("wss://socket.nicemoe.cn")
            logger.info('jx3_api > websockets链接成功！')
            loop.create_task(_task(loop, ws_connect))
            return
        except (ConnectionRefusedError, OSError) as e:
            logger.info(f'jx3_api > [{count}] {e}')
            if count == MAX_RECON_TIMES:
                return
            count += 1
            logger.info(f'jx3_api > [{count}] 尝试向 websockets 服务器建立链接！')
            await asyncio.sleep(10)


async def _task(loop: AbstractEventLoop, ws: websockets):
    global ws_connect
    global ws_echo_list
    try:
        while True:
            data_recv = await ws.recv()
            data = json.loads(data_recv)
            msg_type: int = data['type']
            event = None
            for event_type in Jx3EventList:
                if msg_type == event_type.get_api_type():
                    event = event_type(data)
                    break

            if event is not None:
                if msg_type < 2000:
                    # 处理发送事件，设置user_id或group_id
                    echo = data['echo']
                    for i, echo_one in enumerate(ws_echo_list):
                        if echo == echo_one.echo:
                            event.set_message_type(echo_one)
                            del ws_echo_list[i]

                # 广播事件
                bots = get_bots()
                for _, one_bot in bots.items():
                    await handle_event(one_bot, event)

    except (ConnectionClosed, ConnectionClosedError, ConnectionClosedOK) as e:
        ws_connect = None
        if e.code != 1000:
            logger.error('jx3_api > 链接已断开！')
            loop.create_task(on_connect(loop))
        else:
            logger.error('jx3_api > 链接被服务器关闭！')
        logger.error(e)
