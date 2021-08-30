import httpx

from nonebot.adapters.cqhttp import MessageSegment


# 目前已404，留作备用
def img_from_rosysun():
    r = httpx.get('http://api.rosysun.cn/cos')
    if r.status_code != 200:
        raise Exception('异常返回码')
    else:
        img_url = r.text
        message = MessageSegment.image(img_url)
        return message
