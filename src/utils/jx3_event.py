import time
from typing import Optional

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import overrides
from nonebot.utils import escape_tag


class RecvEvent(BaseEvent):
    '''
    jx3_api的基类事件，推送基类
    '''

    __event__ = "jx3_api"
    message_type: str = "jx3_api"
    post_type: Optional[str]

    @property
    def log(self) -> str:
        '''事件日志内容'''
        return ""

    @classmethod
    def get_api_type(cls):
        return None

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return f'{self.message_type}'+(f'.{self.post_type}'
                                       if self.post_type else '')

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


class OpenServerRecvEvent(RecvEvent):
    '''
    开服提醒事件，服务器主动推送
    '''
    __event__ = "open_server_recv"
    post_type = "open_server_recv"
    server: Optional[str]
    '''服务器名'''
    status: Optional[bool]
    '''服务器状态'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        status = data.get('status')
        self.status = (True if status == 1 else False)

    @overrides(RecvEvent)
    def log(self) -> str:
        if self.status == 1:
            status = "已开服"
        else:
            status = "已维护"
        log = f"开服推送事件：[{self.server}]状态-{status}"
        return log


class NewsRecvEvent(RecvEvent):
    '''
    官方新闻推送事件，服务器主动推送
    '''
    __event__ = "news_recv"
    post_type = "news_recv"
    news_type: Optional[str]
    '''新闻类型'''
    news_tittle: Optional[str]
    '''新闻标题'''
    news_url: Optional[str]
    '''新闻url链接'''
    news_date: Optional[str]
    '''新闻日期'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.news_type = data.get('type')
        self.news_tittle = data.get('title')
        self.news_url = data.get('url')
        self.news_date = data.get('date')

    @overrides
    def log(self) -> str:
        log = f"[{self.news_type}]事件：{self.news_tittle}"
        return log


class AdventureRecvEvent(RecvEvent):
    '''
    奇遇播报事件，服务器主动推送
    '''
    __event__ = "adventure_recv"
    post_type = "adventure_recv"
    server: Optional[str]
    '''服务器名'''
    name: Optional[str]
    '''玩家名'''
    time: Optional[str]
    '''触发时间'''
    serendipity: Optional[str]
    '''奇遇名'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.name = data.get('name')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%m/%d %H:%M', start_trans)
        self.serendipity = data.get('serendipity')

    @overrides(RecvEvent)
    def log(self) -> str:
        log = f"奇遇推送事件：[{self.server}]的[{self.name}]抱走了奇遇：{self.serendipity}"
        return log


class HorseRefreshEvent(RecvEvent):
    '''
    马驹刷新事件
    '''
    __event__ = "horse_refresh"
    post_type = "horse_refresh"
    server: Optional[str]
    '''服务器名'''
    map: Optional[str]
    '''刷新地图'''
    min: Optional[int]
    '''时间范围min'''
    max: Optional[int]
    '''时间范围max'''
    time: Optional[str]
    '''推送时间'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.map = data.get('map')
        self.min = data.get('min')
        self.max = data.get('max')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @overrides(RecvEvent)
    def log(self) -> str:
        log = f"马驹刷新推送：[{self.server}]的[{self.map}]将要在 {str(self.min)}-{str(self.max)} 分后刷新马驹。"
        return log


class HorseCatchedEvent(RecvEvent):
    '''
    马驹被抓事件
    '''
    __event__ = "horse_catched"
    post_type = "horse_catched"
    server: Optional[str]
    '''服务器名'''
    name: Optional[str]
    '''触发角色名'''
    map: Optional[str]
    '''地图'''
    horse: Optional[str]
    '''马驹名'''
    time: Optional[str]
    '''事件时间'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.map = data.get('map')
        self.name = data.get('name')
        self.horse = data.get('horse')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @overrides(RecvEvent)
    def log(self) -> str:
        log = f"马驹被抓事件：[{self.server}]的[{self.name}]在[{self.map}]捕获了 {self.horse} 。"
        return log


class FuyaoRefreshEvent(RecvEvent):
    '''
    扶摇开启事件
    '''
    __event__ = "fuyao_refresh"
    post_type = "fuyao_refresh"
    server: Optional[str]
    '''服务器名'''
    time: Optional[str]
    '''事件时间'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @overrides(RecvEvent)
    def log(self) -> str:
        log = f"扶摇刷新事件：[{self.server}]的扶摇开始刷新 。"
        return log


class FuyaoCatchedEvent(RecvEvent):
    '''
    扶摇点名事件
    '''
    __event__ = "fuyao_catched"
    post_type = "fuyao_catched"
    server: Optional[str]
    '''服务器名'''
    names: Optional[list[str]]
    '''点名角色组'''
    time: Optional[str]
    '''点名时间'''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.names = data.get('name')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @overrides(RecvEvent)
    def log(self) -> str:
        name = ",".join(self.names)
        log = f"扶摇点名事件：[{self.server}]的扶摇点名了，玩家[{name}] 。"
        return log


def create_jx3_event(_type: int, data: dict) -> Optional[RecvEvent]:
    '''根据type值返回事件实例'''
    # 开服推送
    if _type == 2011:
        return OpenServerRecvEvent(data)
    # 新闻推送
    if _type == 2012:
        return NewsRecvEvent(data)
    # 奇遇推送
    if _type == 2000:
        return AdventureRecvEvent(data)
    # 马驹刷新
    if _type == 2001:
        return HorseRefreshEvent(data)
    # 马驹捕获
    if _type == 2002:
        return HorseCatchedEvent(data)
    # 扶摇刷新
    if _type == 2003:
        return FuyaoRefreshEvent(data)
    # 扶摇点名
    if _type == 2004:
        return FuyaoCatchedEvent(data)
    return None
