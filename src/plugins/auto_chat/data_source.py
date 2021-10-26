from typing import Optional

import httpx
from src.modules.group_info import GroupInfo
from src.utils.config import config
from src.utils.log import logger
from src.utils.user_agent import get_user_agent


async def get_active(bot_id: int, group_id: int) -> int:
    '''
    :说明
        获取群里机器人的活跃值

    :参数
        * group_id：QQ群号

    :返回
        * int：活跃度
    '''
    active = await GroupInfo.get_active(bot_id, group_id)
    return active


async def get_saohua() -> str:
    '''
    获取一条骚话
    '''
    jx3_url: str = config.get('jx3-api').get('jx3-url')
    url = f"{jx3_url}/app/random"
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        try:
            req_url = await client.get(url=url)
            req = req_url.json()
            if req['code'] == 200:
                data = req['data']
                msg = data['text']
                log = f'请求骚话成功！内容：{msg}'
                logger.debug(log)
                return msg
        except Exception as e:
            log = f'请求骚话失败，原因：{e}'
            logger.debug(log)
            # 请求失败，从本地返回一条
            msg = "你好骚啊。"
            return msg


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


async def get_image() -> Optional[str]:
    '''
    获取一张图片
    '''
    jx3_url: str = config.get('jx3-api').get('jx3-url')
    url = f"{jx3_url}/share/stickers"
    params = {"format": "json"}
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        try:
            req_url = await client.get(url=url, params=params)
            req = req_url.json()
            if req['code'] == 200:
                data = req['data']
                img_url = data['url']
                log = 'jx3_api请求图片成功'
                logger.debug(log)
                return img_url
            else:
                log = f'jx3_api请求图片失败：{req["msg"]}'
                logger.debug(log)
                return None
        except Exception as e:
            log = f'jx3_api请求图片失败：{e}'
            logger.debug(log)
            return None
