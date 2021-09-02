from nonebot.adapters.cqhttp import Bot
from nonebot.message import handle_event
from .jx3_event import Jx3EventList
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from asyncio import AbstractEventLoop
import websockets
import asyncio
import json

from utils.log import logger


ws_connect = None


async def send_ws_message(msg: dict):
    '''
    使用ws连接发送一条消息
    '''
    global ws_connect
    if ws_connect is not None:
        data = json.dumps(msg)
        await ws_connect.send(data)


async def on_connect(loop: AbstractEventLoop, bot: Bot):
    count = 0
    global ws_connect

    while True:
        try:
            ws_connect = await websockets.connect("wss://socket.nicemoe.cn")
            logger.info('jx3_api > websockets链接成功！')
            loop.create_task(_task(loop, ws_connect, bot))
            return
        except (ConnectionRefusedError, OSError) as e:
            logger.info(f'jx3_api > [{count}] {e}')
            if count == 100:
                return
            count += 1
            logger.info(f'jx3_api > [{count}] 尝试向 websockets 服务器建立链接！')
            await asyncio.sleep(10)


async def _task(loop: AbstractEventLoop, ws: websockets, bot: Bot):
    global ws_connect
    try:
        while True:
            data_recv = await ws.recv()
            data = json.loads(data_recv)
            msg_type = data['type']
            event = None
            for event_type in Jx3EventList:
                if msg_type == event_type.get_api_type():
                    event = event_type(data)
                    break

            if event is not None:
                await handle_event(bot, event)

    except (ConnectionClosed, ConnectionClosedError, ConnectionClosedOK) as e:
        ws_connect = None
        if e.code != 1000:
            logger.error('jx3_api > 链接已断开！')
            loop.create_task(on_connect(loop, bot))
        else:
            logger.error('jx3_api > 链接被服务器关闭！')
        logger.error(e)
