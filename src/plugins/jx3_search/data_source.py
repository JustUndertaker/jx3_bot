import os
import re
import time
from typing import Optional, Tuple

import httpx
from src.modules.group_info import GroupInfo
from src.utils.config import config as baseconfig
from src.utils.utils import nickname

from .config import shuxing, zhiye, zhiye_name

config = baseconfig.get('jx3-api')
'''jx3-api的配置'''

headers = {"ser-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
http_client = httpx.AsyncClient(headers=headers)
'''异步请求库客户端'''

jx3sp_token: Optional[str] = None
'''jx3sp的token'''


async def get_data_from_jx3api(app: str, params: dict, app_type: str = "app") -> Tuple[str, Optional[dict]]:
    '''
    :说明
        发送一条请求给jx3-api，返回结果

    :参数
        * app：请求功能名，链接到url后
        * params：请求参数
        * app_type：默认的网址type，默认为app

    :返回
        * msg：返回msg，为'success'时成功
        * data：返回数据
    '''
    api_url = config.get('jx3-url')
    url = f"{api_url}/{app_type}/{app}"
    try:
        req_url = await http_client.get(url, params=params)
        req = req_url.json()
        msg = req['msg']
        data = req['data']
        return msg, data
    except Exception as e:
        return str(e), None


async def get_server(bot_id: int, group_id: int) -> Optional[str]:
    '''
    获取绑定服务器名称
    '''
    return await GroupInfo.get_server(bot_id, group_id)


async def get_master_server(server: str) -> Optional[str]:
    '''
    获取主服务器名称
    '''
    app = "server"
    params = {
        "name": server
    }
    msg, data = await get_data_from_jx3api(app, params)

    if msg != 'success':
        return None

    server = data.get('server')
    return server


def get_equipquery_name(text: str) -> Tuple[Optional[str], str]:
    '''处理查询装备'''
    text_list = text.split(' ')
    if len(text_list) == 2:
        name = text_list[1]
        server = None
    else:
        server = text_list[1]
        name = text_list[2]
    return server, name


def get_macro_name(text: str) -> str:
    '''宏查询返回职业'''
    args = re.search(r'^[\u4e00-\u9fa5]+宏$', text)
    if args is not None:
        return text[:-1]
    else:
        return text.split(' ')[-1]


def get_qixue_name(text: str) -> str:
    '''奇穴查询返回职业'''
    args = re.search(r'^[\u4e00-\u9fa5]+奇穴$', text)
    if args is not None:
        return text[:-2]
    else:
        return text.split(' ')[-1]


def get_medicine_name(text: str) -> str:
    '''小药查询返回职业'''
    args = re.search(r'^[\u4e00-\u9fa5]+小药$', text)
    if args is not None:
        return text[:-2]
    else:
        return text.split(' ')[-1]


def get_peizhuang_name(text: str) -> str:
    '''配装查询返回职业'''
    args = re.search(r'^[\u4e00-\u9fa5]+配装$', text)
    if args is not None:
        return text[:-2]
    else:
        return text.split(' ')[-1]


def get_gonglue_name(text: str) -> str:
    '''攻略查询返回'''
    args = re.search(r'^[\u4e00-\u9fa5]+攻略$', text)
    if args is not None:
        return text[:-2]
    else:
        return text.split(' ')[-1]


def get_xinfa(name: str) -> str:
    '''获取心法名称'''
    for key, xinfa in zhiye_name.items():
        for one_name in xinfa:
            if one_name == name:
                return key

    # 未找到，返回原值
    return name


def get_daily_week(week: str) -> str:
    '''
    根据星期几返回额外的日常结果
    '''
    daily_list = {
        "一": "帮会跑商：阴山商路(10:00)\n阵营几天：出征祭祀(19:00)\n",
        "二": "阵营攻防：逐鹿中原(20:00)\n",
        "三": "世界首领：少林·乱世，七秀·乱世(20:00)\n",
        "四": "阵营攻防：逐鹿中原(20:00)\n",
        "五": "世界首领：藏剑·乱世，万花·乱世(20:00)\n",
        "六": "攻防前置：南屏山(12:00)\n阵营攻防：浩气盟(13:00，19:00)\n",
        "日": "攻防前置：昆仑(12:00)\n阵营攻防：恶人谷(13:00，19:00)\n"
    }
    return daily_list.get(week)


def hand_adventure_data(data: list[dict]) -> list[dict]:
    '''处理奇遇数据，转换时间'''
    for one_data in data:
        get_time = one_data.get('time')
        if get_time == 0:
            one_data['time'] = "未知"
        else:
            timeArray = time.localtime(get_time)
            one_data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    return data


def _handle_attributes(attribute: dict) -> dict:
    '''预处理attribute'''
    data = {}
    data['score'] = attribute.get('score')
    data['totalLift'] = attribute.get('totalLift')
    data['atVitalityBase'] = attribute.get('atVitalityBase')
    data['atSpiritBase'] = attribute.get('atSpiritBase')
    data['atStrengthBase'] = attribute.get('atStrengthBase')
    data['atAgilityBase'] = attribute.get('atAgilityBase')
    data['atSpunkBase'] = attribute.get('atSpunkBase')
    data['totalAttack'] = attribute.get('totalAttack')
    data['baseAttack'] = attribute.get('baseAttack')
    data['totaltherapyPowerBase'] = attribute.get('totaltherapyPowerBase')
    data['therapyPowerBase'] = attribute.get('therapyPowerBase')
    data['atSurplusValueBase'] = attribute.get('atSurplusValueBase')
    # 会心
    data['atCriticalStrike'] = f"{attribute.get('atCriticalStrike')}（{attribute.get('atCriticalStrikeLevel')}%）"
    # 会效
    data['atCriticalDamagePowerBase'] = f"{attribute.get('atCriticalDamagePowerBase')}（{attribute.get('atCriticalDamagePowerBaseLevel')}%）"
    # 加速
    data['atHasteBase'] = f"{attribute.get('atHasteBaseLevel')}（{attribute.get('atHasteBase')}%）"
    # 破防
    data['atOvercome'] = f"{attribute.get('atOvercome')}（{attribute.get('atOvercomeBaseLevel')}%）"
    # 无双
    data['atStrainBase'] = f"{attribute.get('atStrainBase')}（{attribute.get('atStrainBaseLevel')}%）"
    # 外防
    data['atPhysicsShieldBase'] = f"{attribute.get('atPhysicsShieldBase')}（{attribute.get('atPhysicsShieldBaseLevel')}%）"
    # 内防
    data['atMagicShield'] = f"{attribute.get('atMagicShield')}（{attribute.get('atMagicShieldLevel')}%）"
    # 闪避
    data['atDodge'] = f"{attribute.get('atDodge')}（{attribute.get('atDodgeLevel')}%）"
    # 招架
    data['atParryBase'] = f"{attribute.get('atParryBase')}（{attribute.get('atParryBaseLevel')}%）"
    # 御劲
    data['atToughnessBase'] = f"{attribute.get('atToughnessBase')}（{attribute.get('atToughnessBaseLevel')}%）"
    # 化劲
    data['atDecriticalDamagePowerBase'] = f"{attribute.get('atDecriticalDamagePowerBase')}（{attribute.get('atDecriticalDamagePowerBaseLevel')}%）"

    return data


async def handle_data(alldata: dict) -> dict:
    '''预处理装备数据'''
    sectName = alldata.get("sectName")
    role = f'{alldata.get("forceName")}|{alldata.get("sectName")}'
    body = alldata.get("bodilyName")
    tittle = f'{alldata.get("serverName")}-{alldata.get("roleName")}'

    # 判断职业
    type_data = None
    for key, zhiye_data in zhiye.items():
        for one_data in zhiye_data:
            if one_data == sectName:
                type_data = key
                break
        if type_data is not None:
            break

    if type_data is None:
        type_data = "输出"

    shuxing_data = shuxing.get(type_data)
    num_data = alldata.get("data")
    attribute = num_data.get("attribute")
    post_equip = num_data.get('equip')
    post_qixue = num_data.get('qixue')

    attribute = _handle_attributes(attribute)
    post_attribute = _handle_data(role, body, attribute, shuxing_data)
    # 判断是否需要缓存
    img_cache: bool = baseconfig.get('default').get('img-cache')
    if img_cache:
        post_equip = await _handle_icon(post_equip)
        post_qixue = await _handle_icon(post_qixue)

    post_data = {}
    post_data['tittle'] = tittle
    post_data['nickname'] = nickname
    post_data['attribute'] = post_attribute
    post_data['equip'] = post_equip
    post_data['qixue'] = post_qixue

    return post_data


def _handle_data(role: str, body: str, attribute: dict, shuxing_data: dict) -> list:
    '''处理attribute数据'''
    data = []
    role_dict = {
        "tittle": "角色",
        "value": role
    }
    data.append(role_dict)
    body_dict = {
        "tittle": "体型",
        "value": body
    }
    data.append(body_dict)
    for key, value in shuxing_data.items():
        one_dict = {
            "tittle": value,
            "value": attribute.get(key)
        }
        data.append(one_dict)
    return data


async def _handle_icon(data: list[dict]) -> dict:
    '''处理icon'''
    html_path: str = baseconfig.get('path').get('html')
    icon_path = "."+html_path+"icons/"
    icons_files = os.listdir(icon_path)
    for one_data in data:
        icon_url = one_data.get('icon')
        icon_name = _get_icon_name(icon_url)
        filename = icon_path+icon_name
        if (icon_name in icons_files):
            # 文件已存在，替换url
            icon_file = "icons/"+icon_name
            one_data['icon'] = icon_file
        else:
            # 文件不存在，需要下载
            await _get_icon(icon_url, filename)

    return data


def _get_icon_name(url: str) -> str:
    '''从url返回文件名'''
    url_list = url.split("/")
    last = url_list[-1].split("?")
    return last[0]


async def _get_icon(url: str, filename: str) -> None:
    '''下载icon'''
    req = await http_client.get(url)
    open(filename, 'wb').write(req.content)


def indicator_query_hanlde(data: list[dict]) -> list[dict]:
    '''
    历史战绩预处理数据
    '''
    req_data = []
    for one_data in data:
        one_req_data = {}
        one_req_data['kungfu'] = one_data.get('kungfu')
        pvp_type = one_data.get('pvp_type')
        if pvp_type == 2:
            one_req_data['pvp_type'] = "2v2"
        elif pvp_type == 3:
            one_req_data['pvp_type'] = "3v3"
        else:
            one_req_data['pvp_type'] = "5v5"
        one_req_data['avg_grade'] = one_data.get('avg_grade')
        one_req_data['result'] = one_data.get('won')
        mmr = one_data.get('mmr')
        if mmr > 0:
            mmr_str = "+"+str(mmr)
        else:
            mmr_str = str(mmr)
        one_req_data['source'] = str(one_data.get('total_mmr'))
        one_req_data['source_add'] = mmr_str

        start_time = one_data.get('start_time')
        end_time = one_data.get('end_time')
        time_keep = end_time-start_time
        pvp_time = int((time_keep+30)/60)
        if pvp_time == 0:
            pvp_time = 1
        one_req_data['pvp_time'] = str(pvp_time)+" 分钟"

        time_now = time.time()
        time_ago = time_now-end_time
        if time_ago < 3600:
            # 一小时内用分钟表示
            time_end = int((time_ago+30)/60)
            if time_end == 0:
                time_end = 1
            one_req_data['end_time'] = str(time_end)+" 分钟"
        elif time_ago < 86400:
            # 一天内用小时表示
            time_end = int((time_ago+1800)/3600)
            if time_end == 0:
                time_end = 1
            one_req_data['end_time'] = str(time_end)+" 小时"
        elif time_ago < 864000:
            # 10天内用天表示
            time_end = int((time_ago+43200)/86400)
            if time_end == 0:
                time_end = 1
            one_req_data['end_time'] = str(time_end)+" 天"
        else:
            # 超过10天用日期表示
            timeArray = time.localtime(end_time)
            one_req_data['end_time'] = time.strftime("%Y年%m月%d日", timeArray)

        req_data.append(one_req_data)

    return req_data


async def _get_jx3sp_token() -> Tuple[bool, str]:
    '''
    :说明
        获取jx3sp的token

    :返回
        * bool：是否成功
        * str：返回消息
    '''
    global jx3sp_token
    account = config.get('jx3sp').get('account')
    password = config.get('jx3sp').get('password')
    if account is None or password is None:
        msg = "未配置jx3sp账号密码，请联系服务器管理员"
        return False, msg

    url = "https://www.j3sp.com/api/user/login"
    params = {
        "account": account,
        "password": password
    }
    try:
        req_url = await http_client.get(url, params=params)
        req = req_url.json()
        if req['code'] == 1:
            jx3sp_token = req.get('data').get('userinfo').get('token')
            return True, "success"
        else:
            msg = "jx3sp:"+req['msg']
            return False, msg
    except Exception as e:
        msg = "网络错误，"+str(e)
        return False, msg


async def _check_jx3sp_token() -> Tuple[bool, str]:
    '''
    :说明
        检查jx3sp的token并刷新

    :返回
        * bool：是否成功
        * str：成功为token，不成功为消息
    '''
    global jx3sp_token
    if jx3sp_token is None:
        flag, msg = await _get_jx3sp_token()
        return flag, msg

    url = "https://www.j3sp.com/api/token/check"
    params = {'token': jx3sp_token}
    try:
        req_url = await http_client.get(url, params=params)
        req = req_url.json()
        if req['code'] == 1:
            jx3sp_token = req.get('data').get('token')
            return True, "success"
        else:
            msg = "jx3sp:"+req['msg']
            return False, msg
    except Exception as e:
        msg = "网络错误，"+str(e)
        return False, msg


async def get_jx3sp_img(server: str) -> Tuple[bool, Optional[dict]]:
    '''
    :说明
        获取沙盘数据

    :参数
        * server：服务器名

    :返回
        * bool：是否成功
        * str：成功则为sand_data数据，失败则为返回消息
    '''
    # 验证token
    global jx3sp_token
    flag, msg = await _check_jx3sp_token()
    if not flag:
        return False, msg

    shadow_flag = config.get('jx3sp').get('shadow')
    if shadow_flag:
        shadow = 0
    else:
        shadow = 1
    url = "https://www.j3sp.com/api/sand/"
    params = {
        "token": jx3sp_token,
        "serverName": server,
        "is_history": 0,
        "shadow": shadow
    }
    try:
        req_url = await http_client.get(url, params=params)
        req = req_url.json()
        if req['code'] == 1:
            data = req.get('data').get('sand_data')
            return True, data
        else:
            msg = "jx3sp:"+req['msg']
            return False, msg
    except Exception as e:
        msg = "网络错误，"+str(e)
        return False, msg
