import asyncio
import json
from asyncio import AbstractEventLoop

import websockets
from nonebot import get_bots
from nonebot.message import handle_event
from src.utils.config import config
from src.utils.jx3_event import create_jx3_event
from src.utils.log import logger
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)
from websockets.legacy.client import WebSocketClientProtocol

ws_connect: WebSocketClientProtocol
'''ws全局链接'''

loop: AbstractEventLoop
'''事件循环池'''


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
    global loop
    try:
        while True:
            data_recv = await ws_connect.recv()
            data = json.loads(data_recv)
            msg_type: int = data['type']
            event = create_jx3_event(msg_type, data)

            if event is not None:
                # 服务器推送，对所有机器人广播事件
                logger.debug(event.log())
                bots = get_bots()
                for _, one_bot in bots.items():
                    await handle_event(one_bot, event)

    except (ConnectionClosed, ConnectionClosedError, ConnectionClosedOK) as e:
        if e.code != 1000:
            logger.error('jx3_api > 链接已断开！')
        else:
            logger.error('jx3_api > 链接被关闭！')
        logger.error(e)
