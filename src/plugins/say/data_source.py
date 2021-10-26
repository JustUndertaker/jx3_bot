from typing import Optional

import httpx
from src.utils.config import config
from src.utils.log import logger
from src.utils.user_agent import get_user_agent


async def get_voice(text: str) -> Optional[str]:
    '''
    :说明
        文本转语音

    :参数
        * text：转换内容

    :返回
        * `str`：base64编码内容
        * `None`：转换出错
    '''
    # 判断配置是否完整
    chat_voice = config.get('chat_voice')
    if chat_voice['appkey'] is None or chat_voice['access'] is None or chat_voice['secret'] is None:
        log = "语音配置不完整，请求失败。"
        logger.debug(log)
        return None
    log = f'请求语音合成：{text}'
    logger.debug(log)
    jx3_url: str = config.get('jx3-api').get('jx3-url')
    url = f"{jx3_url}/share/aliyun"
    params = chat_voice.copy()
    params['text'] = text
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        try:
            req_url = await client.get(url=url, params=params)
            req = req_url.json()
            if req['code'] == 200:
                data = req['data']
                voice_url = data['url']
                # 获取语音数据
                return voice_url
            else:
                log = f'语音合成请求参数出错：{req["msg"]}'
                logger.debug(log)
                return None
        except Exception as e:
            log = f'请求链接失败，原因：{e}'
            logger.error(log)
            return None
