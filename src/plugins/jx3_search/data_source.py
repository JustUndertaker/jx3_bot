import re
import time
from typing import Optional, Tuple

import httpx
from src.modules.group_info import GroupInfo
from src.modules.search_record import SearchRecord
from src.modules.token_info import TokenInfo
from src.utils.config import config as baseconfig

from .config import daily_list, jx3_app, zhiye_name

config = baseconfig.get('jx3-api')
'''jx3-api的配置'''

_jx3_token = config.get('jx3-token')
if _jx3_token is None:
    _jx3_token = ""

_jx3_headers = {"token": _jx3_token, "User-Agent": "Nonebot2-jx3_bot"}

jx3_client = httpx.AsyncClient(headers=_jx3_headers)
'''异步请求库客户端'''


async def get_jx3_url(app: str) -> Tuple[str, int]:
    '''
    :说明
        获取访问api的url，如果未配置高级站点地址，则默认采用普通站访问

    :参数
        * app：应用名称

    :返回
        * str：url地址
        * int：cd时间，秒
    '''
    jx3_url: str = config.get('jx3-url')
    get_app: dict = jx3_app.get(app)
    if get_app:
        url = jx3_url+get_app['app']
        cd_time = get_app['cd']
        return url, cd_time

    return "", 0


async def check_cd_time(bot_id: int, group_id: int, app_name: str, cd_time: int) -> Tuple[bool, int]:
    '''
    :说明
        检查模块cd

    :参数
        * bot_id：机器人QQ
        * group_id：QQ群号
        * app_name：查询类型

    :返回
        * bool：检查成功flag
        * int：剩余cd
    '''
    # 没有记录创建记录
    await SearchRecord.append_or_update(bot_id, group_id, app_name)
    time_last = await SearchRecord.get_last_time(bot_id, group_id, app_name)
    time_now = int(time.time())
    over_time = time_now-time_last
    if over_time > cd_time:
        return True, 0
    else:
        left_cd = cd_time-over_time
        return False, left_cd


async def use_one_app(bot_id: int, group_id: int, app_name: str):
    '''记录使用一次查询'''
    await SearchRecord.count_search(bot_id, group_id, app_name)


async def get_data_from_jx3api(url: str, params: dict) -> Tuple[str, Optional[dict]]:
    '''
    :说明
        发送一条请求给jx3-api，返回结果

    :参数
        * url：url地址
        * params：请求参数

    :返回
        * msg：返回msg，为'success'时成功
        * data：返回数据
    '''
    try:
        req_url = await jx3_client.get(url, params=params)
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
    url = config.get('jx3-url')+jx3_app.get('free').get('server')
    params = {
        "name": server
    }
    try:
        req_url = await jx3_client.get(url, params=params)
        req = req_url.json()
        data = req['data']
        return data.get('server')
    except Exception:
        return None


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
    return daily_list.get(week)


def handle_adventure_data(data: list[dict]) -> list[dict]:
    '''处理奇遇数据，转换时间'''
    for one_data in data:
        get_time = one_data.get('time')
        if get_time == 0:
            one_data['time'] = "未知"
        else:
            timeArray = time.localtime(get_time)
            one_data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    return data


async def handle_equip_data(alldata: dict, nickname: str) -> dict:
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
        'value': info.get('score')
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


def handle_awesome_data(match: str, data: list[dict]) -> dict:
    '''
    处理名剑排行数据
    '''
    req_data = {}
    if match == 22:
        req_data['type'] = "2v2"
    elif match == 33:
        req_data['type'] = "3v3"
    else:
        req_data['type'] = "5v5"
    for one_data in data:
        for key, value in one_data.items():
            if value == "":
                one_data[key] = "-"
    req_data['data'] = data
    return req_data


def indicator_query_hanlde(data: list[dict]) -> list[dict]:
    '''
    历史战绩预处理数据
    '''
    req_data = []
    for one_data in data:
        one_req_data = {}
        one_req_data['kungfu'] = one_data.get('kungfu')
        pvp_type = one_data.get('pvpType')
        if pvp_type == 2:
            one_req_data['pvp_type'] = "2v2"
        elif pvp_type == 3:
            one_req_data['pvp_type'] = "3v3"
        else:
            one_req_data['pvp_type'] = "5v5"
        one_req_data['avg_grade'] = one_data.get('avgGrade')
        one_req_data['result'] = one_data.get('won')
        mmr = one_data.get('mmr')
        if mmr > 0:
            mmr_str = "+"+str(mmr)
        else:
            mmr_str = str(mmr)
        one_req_data['source'] = str(one_data.get('totalMmr'))
        one_req_data['source_add'] = mmr_str

        start_time = one_data.get('startTime')
        end_time = one_data.get('endTime')
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


async def _check_token(ticket: str) -> bool:
    '''检测token是否有效'''
    url = config.get('jx3-url')+'/token/validity'
    params = {
        'ticket': ticket
    }
    try:
        req_url = await jx3_client.get(url=url, params=params)
        req = req_url.json()
        code = req['code']
        return (code == 200)
    except Exception:
        return False


async def get_token(bot_id: int) -> Optional[str]:
    '''获取一条token'''
    token_list = await TokenInfo.get_alive_token(bot_id)
    for one_token in token_list:
        # 验证token
        flag = await _check_token(one_token)
        if flag:
            return one_token
        else:
            await TokenInfo.change_alive(bot_id, one_token, False)
    return None
