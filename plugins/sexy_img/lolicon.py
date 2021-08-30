import random

import httpx
from utils.log import logger


'''
api返回格式为
字段名	数据类型	说明
pid	int	作品 pid
p	int	作品所在页
uid	int	作者 uid
title	string	作品标题
author	string	作者名（入库时，并过滤掉 @ 及其后内容）
r18	boolean	是否 R18（在库中的分类，不等同于作品本身的 R18 标识）
width	int	原图宽度 px
height	int	原图高度 px
tags	string[]	作品标签，包含标签的中文翻译（有的话）
ext	string	图片扩展名
uploadDate	number	作品上传日期；时间戳，单位为毫秒
urls	object	包含了所有指定size的图片地址
'''
_url = "https://api.lolicon.app/setu/v2"


async def fetch_lolicon_random_img():
    """
    从lolicon接口获取一张随机色图，并按照规范输出
    """
    j = httpx.get(_url).json()
    error = j['error']
    logger.info(f'请求结果: {j}')
    if len(error) > 0:
        raise Exception(f'接口异常: {error}')
    # 返回图片列表的随机一张图
    data = j['data']
    data_len = len(data)
    if data_len == 0:
        raise Exception(f'返回数据为空')
    # 随机获取一张图片对象
    random_idx = random.randint(0, data_len - 1)
    logger.info(f'随机位置: {random_idx}\n图片列表: {data}')
    item = data[random_idx]
    return item['title'], item["author"], item["urls"]["original"]