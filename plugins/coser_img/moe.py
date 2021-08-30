import httpx
from nonebot.adapters.cqhttp import MessageSegment


def img_from_moe():
    r = httpx.get('https://moe.ci/api.php?return=json')
    if r.status_code != 200:
        raise Exception('异常返回码')
    else:
        json_obj = r.json()
        img_url = json_obj.get('acgUrl', '')
        if len(img_url) <= 0:
            raise Exception('图片为空')
        return MessageSegment.image(img_url)
