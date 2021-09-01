from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.adapters.cqhttp.message import Message
from typing import Optional, Literal
import time


class Event(BaseEvent):
    '''
    jx3_api的基类事件
    '''

    __event__ = "jx3_api"
    message_type: str = "jx3_api"
    post_type: Optional[str]

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


class OpenServerRecvEvent(Event):
    '''
    开服提醒事件，服务器主动推送
    '''
    __event__ = "open_server_recv"
    post_type = "open_server_recv"
    api_type = 2001
    server: Optional[str]
    '''
    服务器名
    '''
    status: Optional[bool]
    '''
    服务器状态
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(OpenServerRecvEvent, self).__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        status = data.get('status')
        self.status = (True if status == 1 else False)


class NewsRecvEvent(Event):
    '''
    官方新闻推送事件，服务器主动推送
    '''
    __event__ = "news_recv"
    post_type = "news_recv"
    api_type = 2002
    news_type: Optional[str]
    '''
    新闻类型，一般为官方新闻
    '''
    news_tittle: Optional[str]
    '''
    新闻标题
    '''
    news_url: Optional[str]
    '''
    新闻url链接
    '''
    news_date: Optional[str]
    '''
    新闻日期
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(NewsRecvEvent, self).__init__()
        data: dict = all_data.get('data')
        self.news_type = data.get('type')
        self.news_tittle = data.get('title')
        self.news_url = data.get('url')
        self.news_date = data.get('news_date')


class AdventureRecvEvent(Event):
    '''
    奇遇播报事件，服务器主动推送
    '''
    __event__ = "adventure_recv"
    post_type = "adventure_recv"
    api_type = 2003
    server: Optional[str]
    '''
    服务器名
    '''
    name: Optional[str]
    '''
    玩家名
    '''
    time: Optional[str]
    '''
    触发时间
    '''
    serendipity: Optional[str]
    '''
    奇遇名
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(AdventureRecvEvent, self).__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.name = data.get('name')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%m/%d %H:%M', start_trans)
        self.serendipity = data.get('serendipity')


class DailyEvent(Event):
    '''
    返回日常事件
    '''
    __event__ = "daily"
    post_type = "daily"
    api_type = 1001
    echo: Optional[int]
    '''
    认证echo
    '''
    DateTime: Optional[str]
    '''
    日期
    '''
    Week: Optional[str]
    '''
    具体周几
    '''
    DayWar: Optional[str]
    '''
    今日大战
    '''
    DayBattle: Optional[str]
    '''
    今日战场
    '''
    DayCommon: Optional[str]
    '''
    公共任务
    '''
    DayCamp: Optional[str]
    '''
    阵营任务
    '''
    DayDraw: Optional[str]
    '''
    美人图
    '''
    WeekCommon: Optional[str]
    '''
    武林通鉴.公共任务
    '''
    WeekFive: Optional[str]
    '''
    武林通鉴.秘境任务
    '''
    WeekTeam: Optional[str]
    '''
    武林通鉴.团队秘境
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(DailyEvent, self).__init__()
        self.echo = all_data.get('echo')
        data: dict = all_data.get('data')
        self.DateTime = data.get('DateTime')
        self.Week = data.get('Week')
        self.DayBattle = data.get('DayBattle')
        self.DayCamp = data.get('DayCamp')
        self.DayCommon = data.get('DayCommon')
        self.DayDraw = data.get('DayDraw')
        self.WeekCommon = data.get('WeekCommon')
        self.WeekFive = data.get('WeekFive')
        self.WeekTeam = data.get('WeekTeam')


class OpenServerSendEvent(Event):
    '''
    返回开服查询结果
    '''
    __event__ = "open_server_send"
    post_type = "open_server_send"
    api_type = 1002
    server: Optional[str]
    '''
    服务器名
    '''
    region: Optional[str]
    '''
    服务器线路
    '''
    status: Optional[bool]
    '''
    服务器状态
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(OpenServerSendEvent, self).__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.region = data.get('region')
        status = data.get('status')
        self.status = (True if status == 1 else False)


class GoldQueryEvent(Event):
    '''
    返回金价查询结果
    '''
    __event__ = "gold_query"
    post_type = "gold_query"
    api_type = 1003
    echo: Optional[int]
    '''
    认证echo
    '''
    server: Optional[str]
    '''
    服务器名
    '''
    price_wanbaolou: Optional[str]
    '''
    金价-万宝楼
    '''
    price_uu898: Optional[str]
    '''
    金价-uu898
    '''
    price_dd373: Optional[str]
    '''
    金价-dd373
    '''
    price_5173: Optional[str]
    '''
    金价-5173
    '''
    price_7881: Optional[str]
    '''
    金价-7881
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(GoldQueryEvent, self).__init__()
        self.echo = all_data.get('echo')
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.price_wanbaolou = data.get('wanbaolou')
        self.price_uu898 = data.get('uu898')
        self.price_dd373 = data.get('dd373')
        self.price_5173 = data.get('5173')
        self.price_7881 = data.get('7881')


class FlowerPriceEvent(Event):
    '''
    返回鲜花价格查询结果
    '''
    __event__ = "flower_price"
    post_type = "flower_price"
    api_type = 1004
    echo: Optional[int]
    '''
    认证echo
    '''
    data: Optional[list[dict]]
    '''
    鲜花数据，是一个字典列表
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(FlowerPriceEvent, self).__init__()
        self.echo = all_data.get('echo')
        self.data = all_data.get('data')


class MatchEquipEvent(Event):
    '''
    返回配装查询结果
    '''
    __event__ = "match_equip"
    post_type = "match_equip"
    api_type = 1006
    echo: Optional[int]
    '''
    认证echo
    '''
    name: Optional[str]
    '''
    心法名称
    '''
    pveUrl: Optional[str]
    '''
    pve装备截图url
    '''
    pvpUrl: Optional[str]
    '''
    pvp装备截图url
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(MatchEquipEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.pveUrl = data.get('pevUrl')
        self.pvpUrl = data.get('pvpUrl')


class MainServerEvent(Event):
    '''
    返回主服务器查询结果
    '''
    __event__ = "main_server"
    post_type = "main_server"
    api_type = 1007
    echo: Optional[int]
    '''
    认证echo
    '''
    name: Optional[str]
    '''
    主服务器名称
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(MainServerEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')


class ExtraPointEvent(Event):
    '''
    返回奇穴查询结果
    '''
    __event__ = "extra_point"
    post_type = "extra_point"
    api_type = 1008
    echo: Optional[int]
    '''
    认证echo
    '''
    name: Optional[str]
    '''
    心法名称
    '''
    longmen: Optional[str]
    '''
    龙门绝境奇穴
    '''
    battle: Optional[str]
    '''
    战场任务奇穴
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(ExtraPointEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.longmen = data.get('longmen')
        self.battle = data.get('battle')
