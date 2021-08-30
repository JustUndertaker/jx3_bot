import httpx
import re
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

from nonebot.adapters.cqhttp.message import MessageSegment
from configs.pathConfig import PATH_PLUGIN_WEATHER, PATH_FONT
from .config import WEATHER_INFO, WIND_INFO


async def get_weather_of_city(city: str) -> MessageSegment:
    '''
    :说明
        通过城市名称获取天气结果

    :参数
        * city：城市名

    :返回
        * message消息内容
    '''
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city
    try:
        data_json = httpx.get(url).json()
        if data_json['desc'] != "OK":
            msg = MessageSegment.text("查询失败了，你看看参数对不对！")
            return msg

        # 消息处理模块
        img = _draw_card_of_weather(data_json['data'])
        msg = MessageSegment.image(img)
        return msg
    except Exception:
        msg = MessageSegment.text("查询失败了，难道是网络有问题！")
        return msg


def _get_temperature(data: str) -> str:
    '''
    :说明
        处理温度字符串

    :参数
        * data：高温 38°C

    :返回
        * str：38°↑
    '''
    level = data[0:2]
    temperature = re.search(r"\d+?\d*", data).group()
    if level == "高温":
        temperature += "°↑"
    else:
        temperature += "°↓"
    return temperature


def _get_fengli(data: str) -> str:
    '''
    :说明
        通过fengli字符串获取风力等级

    :参数
        * data：<![CDATA[2级]]>

    :返回
        * str：2级
    '''
    return data[9:-3]


def _get_date_info(date_str: str) -> str:
    '''
    :说明
        通过字典给定的date，获取具体星期几

    :参数
        * date_str：29日星期四

    :返回
        * str：昨天，今天，星期一...星期天
        * str：日期
    '''
    week_day = date_str[-3:]
    date_day = int(re.search(r"\d+?\d*", date_str).group())
    now_time = datetime.now()
    yesterday = now_time+timedelta(days=-1)
    # 判断是否为昨天
    if date_day == yesterday.day:
        req_date = f"{yesterday.month}/{yesterday.day}"
        return "昨天", req_date

    # 判断是否为今天
    if date_day == now_time.day:
        req_date = f"{now_time.month}/{now_time.day}"
        return "今天", req_date

    # 计算日期
    for i in range(1, 10):
        req_time = now_time+timedelta(days=i)
        if req_time.day == date_day:
            break
    req_date = f"{req_time.month}/{req_time.day}"
    return week_day, req_date


def _create_little_card(data: dict) -> Image:
    '''
    :说明
        创建日期小卡片

    :参数
        * data 一天的数据,包含date,type的key

    :返回
        * Image类
    '''
    week, date = _get_date_info(data['date'])
    weather_type = data['type']
    type_icon = WEATHER_INFO[0]['icon']
    for wearther in WEATHER_INFO:
        # 获取天气图标
        if weather_type == wearther['name']:
            type_icon = wearther['icon']
            break
    icon_path = PATH_PLUGIN_WEATHER+type_icon

    # 新建图像
    size = (50, 120)
    color = (0, 0, 0, 0)
    img = Image.new(mode='RGBA', size=size, color=color)
    drawBoard = ImageDraw.Draw(img)

    # 绘制文字
    font = ImageFont.truetype(PATH_FONT, size=16)
    loc = (0, 0)
    color = (255, 255, 255, 255)
    drawBoard.text(xy=loc, text=week, fill=color, font=font)
    loc = (0, 27)
    drawBoard.text(xy=loc, text=date, fill=color, font=font)
    loc = (0, 90)
    drawBoard.text(xy=loc, text=weather_type, fill=color, font=font)

    # 绘制图标
    img_weather_type = Image.open(icon_path).convert('RGBA')
    size = (24, 24)
    img_weather_type.thumbnail(size)
    loc = (0, 52)
    img.paste(img_weather_type, box=loc, mask=img_weather_type)

    return img


def _draw_card_of_weather(data: dict) -> str:
    '''
    :说明
        根据返回的data画出天气卡片

    :参数
        * data：dict，一天的数据

    :返回
        * 图片文件base64解码后的值，base64://XXXXX
    '''
    # 获取值
    yesterday = data['yesterday']
    city = data['city']
    temperature = data['wendu']+'°'
    weather_type = data['forecast'][0]['type']
    wind_type = data['forecast'][0]['fengxiang']
    wind_level = _get_fengli(data['forecast'][0]['fengli'])
    high = _get_temperature(data['forecast'][0]['high'])
    low = _get_temperature(data['forecast'][0]['low'])

    # 获取配置
    type_icon = WEATHER_INFO[0]['icon']
    background = WEATHER_INFO[0]['background']
    for wearther in WEATHER_INFO:
        # 获取天气图标和背景
        if weather_type == wearther['name']:
            type_icon = wearther['icon']
            background = wearther['background']
            break

    wind_icon = WIND_INFO[0]['icon']
    for wind in WIND_INFO:
        # 获取风向图标
        if wind_type == wind['name']:
            wind_icon = wind['icon']
            break

    icon_path = PATH_PLUGIN_WEATHER+type_icon
    img_path = PATH_PLUGIN_WEATHER+background
    wind_path = PATH_PLUGIN_WEATHER+wind_icon

    # 打开背景图
    img = Image.open(img_path)
    # 设置字体
    font = ImageFont.truetype(PATH_FONT)
    # 设置画板
    drawBoard = ImageDraw.Draw(img)
    MAX_W = 528

    # ------开始绘制----------

    # 城市
    font = ImageFont.truetype(PATH_FONT, size=72)
    w, h = drawBoard.textsize(city, font=font)
    loc = ((MAX_W - w) / 2, 30)
    color = (255, 255, 255, 255)
    drawBoard.text(xy=loc, text=city, fill=color, font=font)

    # 温度
    font = ImageFont.truetype(PATH_FONT, size=137)
    w, h = drawBoard.textsize(temperature, font=font)
    loc = ((MAX_W - w) / 2, 140)
    color = (255, 255, 255, 255)
    drawBoard.text(xy=loc, text=temperature, fill=color, font=font)

    # 最高与最小温度
    font = ImageFont.truetype(PATH_FONT, size=27)
    loc = (390, 180)
    color = (255, 255, 255, 255)
    drawBoard.text(xy=loc, text=high, fill=color, font=font)
    loc = (390, 230)
    drawBoard.text(xy=loc, text=low, fill=color, font=font)

    # 天气类型图标和文字
    img_weather_type = Image.open(icon_path).convert('RGBA')
    size = (48, 48)
    img_weather_type.thumbnail(size)
    loc = (85, 297)
    img.paste(img_weather_type, box=loc, mask=img_weather_type)

    font = ImageFont.truetype(PATH_FONT, size=20)
    loc = (143, 304)
    color = (255, 255, 255, 255)
    drawBoard.text(xy=loc, text=weather_type, fill=color, font=font)

    # 风向图标和文字
    img_wind_type = Image.open(wind_path).convert('RGBA')
    size = (48, 48)
    img_wind_type.thumbnail(size)
    loc = (340, 297)
    img.paste(img_wind_type, box=loc, mask=img_wind_type)

    font = ImageFont.truetype(PATH_FONT, size=20)
    loc = (398, 293)
    color = (255, 255, 255, 255)
    drawBoard.text(xy=loc, text=wind_type, fill=color, font=font)
    loc = (398, 320)
    drawBoard.text(xy=loc, text=wind_level, fill=color, font=font)

    # 绘制6日天气
    loc = (40, 402)
    index = 1
    img_oneday = _create_little_card(yesterday)
    img.paste(img_oneday, box=loc, mask=img_oneday)
    for oneday in data['forecast']:
        loc = (40+80*index, 402)
        img_oneday = _create_little_card(oneday)
        img.paste(img_oneday, box=loc, mask=img_oneday)
        index += 1

    # 返回
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    req_str = 'base64://'+base64_str.decode()

    return req_str


if __name__ == '__main__':
    pass
