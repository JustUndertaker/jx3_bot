from typing import Optional, Tuple

import httpx
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.rule import Rule
from nonebot.typing import T_State
from src.modules.bot_info import BotInfo
from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.log import logger
from src.utils.user_agent import get_user_agent
from src.utils.utils import nickname


def check_event(event_list: list[str]):
    '''
    检查事件
    '''

    async def _check_event(bot: "Bot", event: "Event", state: T_State) -> bool:
        return event.get_event_name() in event_list

    return Rule(_check_event)


async def get_bot_owner(bot_id: int) -> Optional[int]:
    '''获取机器人管理员账号'''
    owner = await BotInfo.get_owner(bot_id)
    return owner


async def set_robot_status(bot_id: int, group_id: int, status: bool) -> bool:
    '''设置机器人开关'''
    return await GroupInfo.set_robot_status(bot_id, group_id, status)


async def get_all_data(bot_id: int) -> list[dict]:
    '''
        :返回所有数据,dict字段：
        * group_id：群号
        * group_name：群名
        * sign_nums：签到数
        * server：服务器名
        * robot_status：运行状态
        * active：活跃值
    '''
    return await GroupInfo.get_all_data(bot_id)


def get_text_num(text: str) -> Tuple[bool, int]:
    '''从信息中获取开关，群号'''
    _status = text.split(' ')[0]
    _group_id = text.split(' ')[1]
    status = (_status == "打开")
    group_id = int(_group_id)
    return status, group_id


async def change_status_all(bot_id: int, status: bool) -> None:
    '''设置所有状态'''
    await GroupInfo.change_status_all(bot_id, status)


async def leave_group(bot_id: int, group_id: int) -> Tuple[bool, str]:
    '''退群，返回[成功flag，群名]'''
    group_name = await GroupInfo.get_group_name(bot_id, group_id)
    if group_name is None:
        group_name = ""
        return False, group_name

    await GroupInfo.delete_one(bot_id=bot_id, group_id=group_id)
    await UserInfo.delete_group(bot_id=bot_id, group_id=group_id)
    return True, group_name


async def get_reply_jx3(question: str) -> Optional[str]:
    '''
    使用jx3_api获取回复
    '''
    # 判断参数是否完整
    chat_nlp = config.get('chat_nlp')
    if chat_nlp['secretId'] is None or chat_nlp['secretKey'] is None:
        log = 'jx3_api接口参数不足，无法请求。'
        logger.debug(log)
        return None

    jx3_url: str = config.get('jx3-api').get('jx3-url')
    url = f"{jx3_url}/share/nlpchat"
    params = chat_nlp.copy()
    params['name'] = nickname
    params['question'] = question
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        try:
            req_url = await client.get(url=url, params=params)
            req = req_url.json()
            if req['code'] == 200:
                log = 'jx3API请求成功。'
                logger.debug(log)
                data = req['data']
                return data['answer']
            else:
                log = f'jx3API请求失败：{req["msg"]}'
                logger.debug(log)
                return None
        except Exception as e:
            log = f'API访问失败：{str(e)}'
            logger.error(log)
            return None


async def get_reply_qingyunke(text: str) -> Optional[str]:
    '''
    :说明
        获取聊天结果，使用青云客的API，备胎

    :参数
        * text：聊天内容

    :返回
        * str：聊天结果

    :异常
        * NetworkError, Exception
    '''
    params = {
        'key': 'free',
        'appid': 0,
        'msg': text
    }
    url = 'http://api.qingyunke.com/api.php'
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        try:
            req_url = await client.get(url, params=params)
            req = req_url.json()
            if req['result'] == 0:
                msg = str(req['content'])
                # 消息替换
                msg = msg.replace(r'{br}', '\n')
                msg = msg.replace('菲菲', nickname)
                log = '请求青云客API成功。'
                logger.debug(log)
                return msg
            else:
                e = req['content']
                log = f'青云客API请求失败：{e}'
                logger.error(log)
                return None
        except Exception as e:
            log = f'青云客API访问失败：{str(e)}'
            logger.error(log)
            return None


def handle_borad_message(all: bool, one_message: MessageSegment) -> Tuple[MessageSegment, Optional[int]]:
    '''
    处理广播消息第一条参数问题，非全体广播会返回group_id
    '''
    text: str = one_message.data['text']
    if all:
        # 全体广播
        req_text = text[5:]
        req_msg = MessageSegment.text(req_text)
        req_group_id = None
    else:
        # 单体广播
        text_list = text.split(' ')
        req_group_id = int(text_list[1])
        if len(text_list) > 2:
            req_text = " "
            req_text = req_text.join(text_list[2:])
        else:
            req_text = ""
        req_msg = MessageSegment.text(req_text)
    return req_msg, req_group_id
