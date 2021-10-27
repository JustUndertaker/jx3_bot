import re
import time
from typing import Optional, Tuple

import httpx
from src.modules.bot_info import BotInfo
from src.modules.group_info import GroupInfo
from src.utils.config import config as baseconfig
from src.utils.utils import nickname

from .config import jx3_app, zhiye_name

config = baseconfig.get('jx3-api')
'''jx3-api的配置'''

_jx3_token = config.get('jx3-token')
_jx3_vip_token = config.get('jx3-vip-token')

_jx3_headers = {"token": _jx3_token, "User-Agent": "Nonebot2-jx3_bot"}
_jx3_vip_headers = {"token": _jx3_vip_token, "User-Agent": "Nonebot2-jx3_bot"}

jx3_client = httpx.AsyncClient(headers=_jx3_headers)
'''异步请求库客户端'''
jx3_vip_client = httpx.AsyncClient(headers=_jx3_vip_headers)
'''异步请求库客户端'''

jx3sp_token: Optional[str] = None
'''jx3sp的token'''
_j3sp_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
http_client = httpx.AsyncClient(headers=_j3sp_headers)


async def get_jx3_url(bot_id: int, app: str) -> Tuple[bool, str]:
    '''
    :说明
        获取访问api的url，如果未配置高级站点地址，则默认采用普通站访问

    :参数
        * bot_id：机器人QQ
        * app：应用名称

    :返回
        * bool：是否为高级用户
        * str：url地址
    '''
    jx3_url = config.get('jx3-url')
    vip_url = config.get('jx3-vip-url')
    app_dict = jx3_app.get(app)
    if vip_url is None:
        url = jx3_url+app_dict.get('free')
        return False, url

    permission = await BotInfo.bot_get_permission(bot_id)
    if permission:
        url = vip_url+app_dict.get('vip')
    else:
        url = jx3_url+app_dict.get('free')

    return permission, url


async def get_data_from_jx3api(url: str, params: dict, vip_flag: bool) -> Tuple[str, Optional[dict]]:
    '''
    :说明
        发送一条请求给jx3-api，返回结果

    :参数
        * url：url地址
        * params：请求参数
        * vip_flag：是否为高级用户

    :返回
        * msg：返回msg，为'success'时成功
        * data：返回数据
    '''
    if vip_flag:
        client = jx3_vip_client
    else:
        client = jx3_client
    try:
        req_url = await client.get(url, params=params)
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
    app = "/app/server"
    url = config.get('jx3-url')+app
    params = {
        "name": server
    }
    msg, data = await get_data_from_jx3api(url, params, False)

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


async def handle_equip_data(alldata: dict) -> dict:
    '''预处理装备数据'''
    kungfu = alldata.get("kungfu")
    tittle = f'{alldata.get("serverName")}-{alldata.get("roleName")}'

    # 处理属性
    post_attribute = []

    kungfu = {
        'name': '心法',
        'value': alldata.get("kungfu")
    }
    post_attribute.append(kungfu)

    info = alldata.get('info')
    score = {
        'name': '装分',
        'value': info.get('totalScore')
    }
    post_attribute.append(score)

    panel: list[dict] = info.get('panel')
    for one_data in panel:
        one_dict = {}
        one_dict['name'] = one_data.get('name')
        percent = one_data.get('percent')
        value = one_data.get('value')
        if percent:
            one_dict['value'] = f"{value}%"
        else:
            one_dict['value'] = value
        post_attribute.append(one_dict)

    # 奇穴
    qixue: list[dict] = alldata.get('qixue')
    post_qixue = []
    for one_data in qixue:
        one_dict = {}
        one_dict['name'] = one_data.get('name')
        one_dict['icon'] = one_data.get('icon')
        post_qixue.append(one_dict)

    # 装备
    equip: list[dict] = alldata.get('equip')
    post_equip = []
    for one_data in equip:
        one_dict = {}
        one_dict['name'] = one_data.get('name')
        one_dict['icon'] = one_data.get('icon')
        post_equip.append(one_dict)

    post_data = {}
    post_data['tittle'] = tittle
    post_data['nickname'] = nickname
    post_data['attribute'] = post_attribute
    post_data['equip'] = post_equip
    post_data['qixue'] = post_qixue

    return post_data


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
