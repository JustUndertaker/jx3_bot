import httpx
from io import BytesIO
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from nonebot.adapters.cqhttp.message import MessageSegment
from configs.pathConfig import YIQING_IMG_PATH, PATH_FONT
from utils.user_agent import get_user_agent


async def get_yiqing_card(province: str, city: str = None) -> MessageSegment:
    '''
    :说明
        * 获取疫情卡片

    :参数
        * province：省名称
        * city：城市名称

    :返回
        * message
    '''

    try:
        data = await _get_yiqing_data(province, city)
    except:
        msg = "访问网络出错了。"
        return MessageSegment.text(msg)

    # 开始造卡
    img = await _draw_card(data)

    # 返回
    return MessageSegment.image(img)


async def _get_yiqing_data(province: str, city: str = None) -> dict:
    '''
    :说明
        * 查询城市疫情数据

    :参数
        * province：省名称
        * city：城市名，可为空

    :返回
        * dict：疫情数据字典
    '''
    url = "https://api.yimian.xyz/coro"

    if city is None:
        params = {"province": province}
    else:
        params = {
            "province": province,
            "city": city
        }

    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        resp = await client.get(url, params=params)
        result = resp.json()
    data = {}
    if city is None:
        # 查询省份
        data['name'] = result['provinceName']
    else:
        # 查询城市
        data['name'] = result['cityName']
    data['currentConfirmedCount'] = result['currentConfirmedCount']  # 现存确诊
    data['confirmedCount'] = result['confirmedCount']  # 累计确诊
    data['suspectedCount'] = result['suspectedCount']  # 疑似病例
    data['curedCount'] = result['curedCount']  # 累计治愈
    data['deadCount'] = result['deadCount']  # 累计死亡
    data['highDangerCount'] = result['highDangerCount']  # 重症病例

    return data


async def _draw_card(data: dict) -> str:
    '''
    :说明
        * 绘制疫情卡片

    :参数
        * data：疫情数据

    :返回
        * 图片文件base64解码后的值，base64://XXXXX
    '''
    # 获取数据
    name = data['name']  # 城市名称
    currentConfirmedCount = str(data['currentConfirmedCount'])  # 现存确诊
    confirmedCount = str(data['confirmedCount'])  # 累计确诊
    suspectedCount = str(data['suspectedCount'])  # 疑似病例
    curedCount = str(data['curedCount'])  # 累计治愈
    deadCount = str(data['deadCount'])  # 累计死亡
    highDangerCount = str(data['highDangerCount'])  # 重症病例

    # 打开文件
    img_path = YIQING_IMG_PATH
    img = Image.open(img_path)
    # 设置字体
    font = ImageFont.truetype(PATH_FONT)
    # 设置画板
    drawBoard = ImageDraw.Draw(img)

    # ===============开始绘制======================================

    # 城市
    font = ImageFont.truetype(PATH_FONT, size=28)
    loc = (86, 72)
    color = (79, 126, 237, 255)
    drawBoard.text(xy=loc, text=name, fill=color, font=font)

    # 日期
    today = datetime.today().strftime('%Y-%m-%d')
    font = ImageFont.truetype(PATH_FONT, size=20)
    loc = (320, 87)
    color = (79, 126, 237, 255)
    drawBoard.text(xy=loc, text=today, fill=color, font=font)

    # 现存确诊
    font = ImageFont.truetype(PATH_FONT, size=18)
    w, h = font.getsize(currentConfirmedCount)
    loc = (118-int(w/2), 150)
    color = (251, 51, 53, 255)
    drawBoard.text(xy=loc, text=currentConfirmedCount, fill=color, font=font)

    # 疑似病例
    w, h = font.getsize(suspectedCount)
    loc = (263-int(w/2), 150)
    color = (251, 51, 53, 255)
    drawBoard.text(xy=loc, text=suspectedCount, fill=color, font=font)

    # 重症病例
    w, h = font.getsize(highDangerCount)
    loc = (400-int(w/2), 150)
    color = (134, 22, 24, 255)
    drawBoard.text(xy=loc, text=highDangerCount, fill=color, font=font)

    # 累计确诊
    w, h = font.getsize(confirmedCount)
    loc = (118-int(w/2), 213)
    color = (176, 1, 2, 255)
    drawBoard.text(xy=loc, text=confirmedCount, fill=color, font=font)

    # 累计死亡
    w, h = font.getsize(deadCount)
    loc = (263-int(w/2), 213)
    color = (77, 77, 77, 255)
    drawBoard.text(xy=loc, text=deadCount, fill=color, font=font)

    # 累计治愈
    w, h = font.getsize(curedCount)
    loc = (400-int(w/2), 213)
    color = (47, 173, 149, 255)
    drawBoard.text(xy=loc, text=curedCount, fill=color, font=font)

    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    req_str = 'base64://'+base64_str.decode()

    return req_str
