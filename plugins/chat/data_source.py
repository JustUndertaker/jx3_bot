import json
import time
import httpx
from httpx import NetworkError
from nonebot.adapters.cqhttp import MessageSegment

from .tecent_api import get_authorization
from configs.config import SECRET_ID, SECRET_KEY
from utils.log import logger


async def get_chat_reply(text: str) -> MessageSegment:
    '''
    :说明
        获得聊天内容

    :参数
        * 聊天内容

    :返回
        * 聊天结果

    :异常
        * Exception
    '''

    if SECRET_ID != '' and SECRET_KEY != '':
        try:
            # 先调用腾讯接口
            req = _get_chat_from_tencent(text)
            msg = MessageSegment.text(req)
            log = f'闲聊-腾讯API返回：{req}'
            logger.info(log)
            return msg

        except Exception:
            error = '闲聊-腾讯接口调用失败了，改用青云客接口。'
            logger.error(error)

    # 调用青云客API
    try:
        req = _get_chat_from_qingyunke(text)
        msg = MessageSegment.text(req)
        log = f'闲聊-青云客API返回：{req}'
        logger.info(log)
        return msg
    except NetworkError:
        error = '闲聊-青云客接口调用失败：网络问题'
        logger.error(error)
        raise NetworkError
    except Exception:
        error = '闲聊-青云客接口调用失败：其他问题'
        logger.error(error)
        raise Exception


def _get_chat_from_tencent(text: str) -> str:
    '''
    :说明
        获取聊天结果，使用腾讯云的API

    :参数
        * text：聊天内容

    :返回
        * str：聊天结果

    :异常
        * NetworkError, Exception
    '''

    data = {'Query': text}
    data = json.dumps(data)
    host = "nlp.tencentcloudapi.com"
    url = "https://" + host
    timestamp = int(time.time())
    authorization = get_authorization(timestamp, data, SECRET_ID, SECRET_KEY)

    headers = {
        'X-TC-Action': 'ChatBot',
        'X-TC-Version': '2019-04-08',
        'X-TC-Region': 'ap-guangzhou',
        'X-TC-Timestamp': str(timestamp),
        'X-TC-Language': 'zh-CN',
        'Authorization': authorization,
        'Host': host,
        'Content-Type': 'application/json'
    }
    try:
        req = httpx.post(url, data=data, headers=headers).json()['Response']
        if 'Error' in req:
            raise Exception
        else:
            reply = req['Reply']
            return reply
    except Exception:
        raise NetworkError


def _get_chat_from_qingyunke(text: str) -> str:
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
    try:
        req = httpx.get(url, params=params).json()
        if req['result'] != 0:
            raise Exception
        msg = str(req['content'])
        msg = msg.replace(r'{br}', '\n')
        return msg
    except Exception:
        raise NetworkError
