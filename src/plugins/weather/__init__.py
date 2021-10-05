import base64
import re
from io import BytesIO

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.plugin import export
from PIL import Image

from .convrt_pic import draw
from .get_weather import get_City_Weather

export = export()
export.plugin_name = '天气查询'
export.plugin_usage = '查询城市天气。'
export.ignore = False  # 插件管理器忽略此插件


weather = on_regex(r".*?(.*)天气.*?", priority=1)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


def get_msg(msg) -> str:
    msg1 = re.search(r".*?(.*)天气.*?", msg)
    msg2 = re.search(r".*?天气(.*).*?", msg)
    msg1 = msg1.group(1).replace(" ", "")
    msg2 = msg2.group(1).replace(" ", "")
    msg = msg1 if msg1 else msg2

    return msg


@weather.handle()
async def _(bot: Bot, event: MessageEvent):
    city = get_msg(event.get_plaintext())
    if city:
        try:
            data = await get_City_Weather(city)
            img = draw(data)
            b64 = img_to_b64(img)
            await weather.finish(MessageSegment.image(b64))
        except Exception:
            pass
    else:
        await weather.finish("地点是...空气吗?? >_<")
