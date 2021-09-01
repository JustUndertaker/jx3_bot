from nonebot.adapters.cqhttp import Bot
from nonebot.message import handle_event
from .jx3_event import OpenServerEvent, NewsEvent, AdventureEvent
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from asyncio import AbstractEventLoop
import websockets
import asyncio
import json

from utils.log import logger


async def on_connect(loop: AbstractEventLoop, bot: Bot):
    count = 0

    while True:
        try:
            ws = await websockets.connect("wss://socket.nicemoe.cn")
            logger.info('jx3_api > websockets链接成功！')
            loop.create_task(_task(loop, ws, bot))
            return
        except (ConnectionRefusedError, OSError) as e:
            logger.info(f'jx3_api > [{count}] {e}')
            if count == 100:
                return
            count += 1
            logger.info(f'jx3_api > [{count}] 尝试向 websockets 服务器建立链接！')
            await asyncio.sleep(10)


async def _task(loop: AbstractEventLoop, ws: websockets, bot: Bot):
    try:
        while True:
            data_recv = await ws.recv()
            data = json.loads(data_recv)
            msg_type = data['type']
            event = None
            if msg_type == 2001:
                event = OpenServerEvent(data)
                # event.set_event_data(data=data)
            if msg_type == 2002:
                event = NewsEvent(data)
                # event.set_event_data(data=data)
            if msg_type == 2003:
                event = AdventureEvent(data)
                # event.set_event_data(data=data)

            if event is not None:
                await handle_event(bot, event)

    except (ConnectionClosed, ConnectionClosedError, ConnectionClosedOK) as e:
        if e.code != 1000:
            logger.error('jx3_api > 链接已断开！')
            loop.create_task(on_connect(loop, bot))
        else:
            logger.error('jx3_api > 链接被服务器关闭！')
        logger.error(e)
