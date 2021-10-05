import base64
import re
from io import BytesIO

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import export
from PIL import Image

from .convrt_pic import draw
from .get_weather import get_City_Weather

export = export()
export.plugin_name = '天气查询'
export.plugin_usage = '查询城市天气。'
export.ignore = False  # 插件管理器忽略此插件


weather_regex = r"([\u4e00-\u9fa5]+天气$)|(^天气 [\u4e00-\u9fa5]+$)"
weather = on_regex(pattern=weather_regex, permission=GROUP, priority=5, block=True)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


def _get_msg(message_str: str) -> str:
    # 匹配前面
    args = re.search(r'[\u4e00-\u9fa5]+天气$', message_str)
    if args is not None:
        # 获得字符串
        loc = re.search('天气', args.string).span()[0]
        args = args.string[0:loc]
        # 去除前缀
        head = re.search(r'(查一下)|(问一下)|(问问)|(想知道)|(查询)|(查查)', args)
        if head is not None:
            loc = head.span()[1]
            args = args[loc:]
        return args
    else:
        # 匹配后面
        loc = re.search('天气 ', message_str).span()[1]
        return message_str[loc:]


@weather.handle()
async def _(bot: Bot, event: MessageEvent):
    city = _get_msg(event.get_plaintext())

    code, data = await get_City_Weather(city)
    if code == "200":
        img = draw(data)
        b64 = img_to_b64(img)
        msg = MessageSegment.image(b64)
    elif code == "404":
        msg = "查询失败，请输入正确的城市名称。"
    elif code == "401":
        msg = "查询失败，apikey不正确，请联系服务器管理员。"
    else:
        msg = f"查询失败，code：{code}"
    await weather.finish(msg)
