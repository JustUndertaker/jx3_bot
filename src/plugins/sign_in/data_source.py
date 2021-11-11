import base64
import random
from datetime import date

import httpx
from nonebot.adapters.cqhttp import Message, MessageSegment
from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo
from src.utils.user_agent import get_user_agent

from .config import FRIENDLY_ADD, GOLD_BASE, LUCKY_GOLD, LUCKY_MAX, LUCKY_MIN


async def get_sign_in(bot_id: int, user_id: int, group_id: int, user_name: str) -> Message:
    '''
    :说明
        用户签到

    :参数
        * bot_id：机器人QQ
        * user_id：用户QQ
        * group_id：QQ群号
        * user_name：用户昵称

    :返回
        * MessageSegment：机器人返回消息
    '''
    # 获取上次签到日期
    last_sign = await UserInfo.get_last_sign(bot_id, user_id, group_id)
    # 判断是否已签到
    today = date.today()
    if today == last_sign:
        msg = MessageSegment.text('你今天已经签到了。')
        return msg

    # 头像
    qq_head = await _get_qq_img(user_id)
    msg_head = MessageSegment.image(qq_head)

    # 设置签到日期
    await UserInfo.sign_in(bot_id, user_id, group_id)

    # 签到名次
    await GroupInfo.sign_in_add(bot_id, group_id)
    sign_num = await GroupInfo.get_sign_nums(bot_id, group_id)

    # 计算运势
    lucky = random.randint(LUCKY_MIN, LUCKY_MAX)
    await UserInfo.change_lucky(bot_id, user_id, group_id, lucky)

    # 计算金币
    gold = GOLD_BASE+lucky*LUCKY_GOLD
    await UserInfo.change_gold(bot_id, user_id, group_id, gold)
    gold_all = await UserInfo.get_gold(bot_id, user_id, group_id)

    # 好友度
    friendly_add = FRIENDLY_ADD
    await UserInfo.change_friendly(bot_id, user_id, group_id, friendly_add)
    friendly = await UserInfo.get_friendly(bot_id, user_id, group_id)

    # 累计签到次数
    sign_times = await UserInfo.get_sign_times(bot_id, user_id, group_id)

    # 更新用户昵称
    await UserInfo.set_user_name(bot_id, user_id, group_id, user_name)

    msg_txt = f'本群第 {sign_num} 位 签到完成\n'
    msg_txt += f'今日运势：{lucky}\n'
    msg_txt += f'获得金币：+{gold}（总金币：{gold_all}）\n'
    msg_txt += f'当前好感度：{friendly}\n'
    msg_txt += f'累计签到次数：{sign_times}'
    msg = msg_head+MessageSegment.text(msg_txt)
    return msg


async def _get_qq_img(user_id: int) -> str:
    '''
    :说明
        获取QQ头像

    :参数
        * user_id：用户QQ

    :返回
        * Base64编码后的str
    '''
    num = random.randrange(1, 4)
    url = f'http://q{num}.qlogo.cn/g'
    params = {
        'b': 'qq',
        'nk': user_id,
        's': 100
    }
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        resp = await client.get(url, params=params)

    req_bytes = resp.content
    base64_str = base64.b64encode(req_bytes)
    req_str = 'base64://'+base64_str.decode()
    return req_str
