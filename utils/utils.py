import nonebot
from .ap_scheduler import APSscheduler

# 全局定时器对象
scheduler = APSscheduler


def get_bot():
    '''
    全局获取bot对象
    '''
    return list(nonebot.get_bots().values())[0]
