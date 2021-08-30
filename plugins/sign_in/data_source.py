import random
from datetime import date
import httpx
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from utils.log import logger

from nonebot.adapters.cqhttp.message import MessageSegment
from modules.user_info import UserInfo
from modules.group_info import GroupInfo
from utils.user_agent import get_user_agent
from utils.image import draw_border_text, img_square_to_circle
from configs.pathConfig import SIGN_IN_IMG_PATH, PATH_FONT
from .config import (
    LUCKY_MIN,
    LUCKY_MAX,
    FRIENDLY_ADD,
    GOLD_BASE,
    LUCKY_GOLD,
    RANDOM_SAID
)


async def reset() -> list:
    '''
    :说明
        重置签到人数，返回所有群号list
    '''
    await GroupInfo.reset_sign()
    group_list = await GroupInfo.get_group_list()
    return group_list


async def update_info(group_id: int, member_list: list) -> MessageSegment:
    '''
    :说明
        * 更新群信息
    '''
    for one in member_list:
        user_id = one['user_id']
        user_name = one['card']
        if user_name == '':
            user_name = one['nickname']
        await UserInfo.append_or_update(user_id, group_id, user_name)
    await GroupInfo.append_or_update(group_id)
    msg = MessageSegment.text('群信息更新完毕。')
    return msg


async def get_sign_in(user_id: int, group_id: int, user_name: str) -> MessageSegment:
    '''
    :说明
        用户签到

    :参数
        * user_id：用户QQ
        * group_id：QQ群号
        * user_name：用户昵称

    :返回
        * MessageSegment：机器人返回消息
    '''
    # 更新记录
    await UserInfo.append_or_update(user_id, group_id, user_name)
    await GroupInfo.append_or_update(group_id)

    # 获取上次签到日期
    last_sign = await UserInfo.get_last_sign(user_id, group_id)
    # 判断是否已签到
    today = date.today()
    if today == last_sign:
        msg = MessageSegment.text('你今天已经签到了。')
        return msg

    # 设置签到日期
    await UserInfo.sign_in(user_id, group_id)

    # 签到名次
    await GroupInfo.sign_in_add(group_id)
    sign_num = await GroupInfo.get_sign_nums(group_id)

    # 计算运势
    lucky = random.randint(LUCKY_MIN, LUCKY_MAX)
    await UserInfo.change_lucky(user_id, group_id, lucky)

    # 计算金币
    gold = GOLD_BASE+lucky*LUCKY_GOLD
    await UserInfo.change_gold(user_id, group_id, gold)

    # 好友度
    friendly_add = FRIENDLY_ADD
    await UserInfo.change_friendly(user_id, group_id, friendly_add)
    friendly = await UserInfo.get_friendly(user_id, group_id)

    # 累计签到次数
    sign_times = await UserInfo.get_sign_times(user_id, group_id)

    # 可能出现访问出错，这时改为文字发送信息
    try:
        msg = await _draw_card(user_id, user_name, sign_num, lucky, gold, friendly, sign_times)
        log = '签到卡片创建成功。'
        logger.debug(log)
        msg = MessageSegment.at(user_id)+msg
    except Exception:
        log = '签到卡片创建失败。'
        logger.debug(log)
        req = f'\n签到成功。今日运势：{lucky}\n获得金币：{gold}\n累计签到次数：{sign_times}'
        msg = MessageSegment.at(user_id)+MessageSegment.text(req)
    return msg


async def _draw_card(user_id: int, user_name: str, sign_num: int, lucky: int, gold: int, friendly: int, sign_times: int) -> MessageSegment:
    '''
    :说明
        画出签到卡片

    :参数
        * user_id：用户QQ
        * user_name：用户名称
        * sign_num：签到名次
        * lucky：幸运值
        * gold：获得金币
        * friendly：当前好感度
        * sign_times：累计签到次数

    :返回
        * Message信息
    '''
    # 获取背景图
    img = Image.new('RGBA', (640, 640), (255, 255, 255, 255))

    # 粘贴头像
    img_head = await _get_qq_img(user_id)
    w, h = img_head.size
    img_gauss = img_head.filter(ImageFilter.GaussianBlur(radius=4))

    # 粘贴背景
    loc = (320-int(w/2), 320-int(h/2))
    img.paste(img_gauss, loc)

    # 开始操作
    font = ImageFont.truetype(PATH_FONT, size=25)
    color = (243, 52, 52)
    bp_color = (255, 255, 255)
    # 用户名
    img_name = draw_border_text(user_name, font, 2, color, bp_color)
    w, _ = font.getsize(user_name)
    loc = (320-int(w/2), 80)
    img.paste(img_name, loc, img_name)

    # 头像
    border_color = (211, 170, 30)
    try:
        size = (167, 167)
        little_head = img_head.resize(size)
        head = img_square_to_circle(little_head, 167, 15, border_color)
    except Exception:
        w, h = img_head.size
        if w > h:
            radius = h
        else:
            radius = w
        head = img_square_to_circle(img_head, radius, 2, border_color)
    loc = (222, 130)
    img.paste(head, loc, mask=head)

    # 小卡片
    img_card = _draw_sign_in(str(sign_num), str(lucky), str(gold), str(friendly), str(sign_times))
    loc = (79, 265)
    img.paste(img_card, loc, mask=img_card)

    # 语录
    random_text = random.choice(RANDOM_SAID)
    w, _ = font.getsize(random_text)
    loc = (320-int(w/2), 578)
    img_yulu = draw_border_text(random_text, font, 2, color, bp_color)
    img.paste(img_yulu, loc, img_yulu)

    # 返回
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    req_str = 'base64://'+base64_str.decode()

    return MessageSegment.image(req_str)


async def _get_qq_img(user_id: int) -> Image:
    '''
    :说明
        获取QQ头像

    :参数
        * user_id：用户QQ

    :返回
        * Image类
    '''
    url = 'http://q1.qlogo.cn/g'
    params = {
        'b': 'qq',
        'nk': user_id,
        's': 640
    }
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        resp = await client.get(url, params=params)

    tempIm = BytesIO(resp.content)
    img = Image.open(tempIm)
    return img


def _draw_sign_in(sign_num: str, lucky: str, gold: str, friendly: str, sign_times: str) -> Image:
    '''
    :说明
        绘制签到小卡片
    '''
    # 打开背景图
    img = Image.open(SIGN_IN_IMG_PATH)
    img_draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype(PATH_FONT, size=25)
    color = (243, 52, 52)

    # 签到名次
    w, _ = font.getsize(sign_num)
    loc = (204-w/2, 62)
    img_draw.text(loc, sign_num, color, font)

    # 气运
    loc = (283, 100)
    img_draw.text(loc, lucky, color, font)

    # 金币
    loc = (283, 143)
    img_draw.text(loc, gold, color, font)

    # 好感度
    loc = (283, 186)
    img_draw.text(loc, friendly, color, font)

    # 签到次数
    loc = (283, 230)
    img_draw.text(loc, sign_times, color, font)

    return img
