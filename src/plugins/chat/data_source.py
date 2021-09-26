from typing import Optional

import httpx
from configs.config import CHAT_NLP
from utils.log import logger
from utils.user_agent import get_user_agent
from utils.utils import nickname


async def get_reply_jx3(question: str) -> Optional[str]:
    '''
    使用jx3_api获取回复
    '''
    # 判断参数是否完整
    if CHAT_NLP['secretId'] == "" or CHAT_NLP['secretKey'] == "":
        log = 'jx3_api接口参数不足，无法请求。'
        logger.debug(log)
        return None

    url = "https://www.jx3api.com/extend/nlpchat"
    params = CHAT_NLP.copy()
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
            log = f'API访问失败：{e}'
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
            log = f'青云客API访问失败：{e}'
            logger.error(log)
            return None
