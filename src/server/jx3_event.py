import time
from typing import Optional, Union

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import overrides
from nonebot.utils import escape_tag


class WS_ECHO():
    '''
    维护连接池数据
    '''
    echo: int
    '''
    认证echo
    '''
    bot_id: str
    '''
    机器人id，适配nb2，使用str
    '''
    user_id: Optional[int]
    '''
    私聊消息：QQ号
    '''
    group_id: Optional[int]
    '''
    群消息：QQ群号
    '''
    server: Optional[str]
    '''
    服务器
    '''
    params: Optional[str]
    '''
    额外参数
    '''

    def __init__(self, echo: int,
                 bot_id: str,
                 user_id: Optional[int] = None,
                 group_id: Optional[int] = None,
                 server: Optional[str] = None,
                 params: Optional[str] = None):
        self.echo = echo
        self.bot_id = bot_id
        self.user_id = user_id
        self.group_id = group_id
        self.server = server
        self.params = params


class RecvEvent(BaseEvent):
    '''
    jx3_api的基类事件，推送基类
    '''

    __event__ = "jx3_api"
    message_type: str = "jx3_api"
    post_type: Optional[str]

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


class SendEvent(BaseEvent):
    '''
    jx3_api的基类事件，发送基类
    '''

    __event__ = "jx3_api"
    message_type: str = "jx3_api"
    post_type: Optional[str]
    user_id: Optional[int]
    group_id: Optional[int]
    server: Optional[str]
    '''服务器'''
    echo: Optional[int]
    '''
    会话echo
    '''
    msg_success: Optional[str]
    '''
    是否查询成功，成功为sucess，失败为其他
    '''
    params: Optional[str]
    '''
    额外参数
    '''

    def set_message_type(self, ws_econ: WS_ECHO):
        self.user_id = ws_econ.user_id
        self.group_id = ws_econ.group_id
        self.server = ws_econ.server
        self.params = ws_econ.params

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
        return str(self.user_id)

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
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        status = data.get('status')
        self.status = (True if status == 1 else False)

    @classmethod
    def get_api_type(cls):
        return 2001


class NewsRecvEvent(RecvEvent):
    '''
    官方新闻推送事件，服务器主动推送
    '''
    __event__ = "news_recv"
    post_type = "news_recv"
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
        super().__init__()
        data: dict = all_data.get('data')
        self.news_type = data.get('type')
        self.news_tittle = data.get('title')
        self.news_url = data.get('url')
        self.news_date = data.get('date')

    @classmethod
    def get_api_type(cls):
        return 2002


class AdventureRecvEvent(RecvEvent):
    '''
    奇遇播报事件，服务器主动推送
    '''
    __event__ = "adventure_recv"
    post_type = "adventure_recv"
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
        super().__init__()
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.name = data.get('name')
        get_time = data.get('time')
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%m/%d %H:%M', start_trans)
        self.serendipity = data.get('serendipity')

    @classmethod
    def get_api_type(cls):
        return 2003


class EquipQueryEvent(SendEvent):
    '''
    返回角色装备查询结果
    '''
    __event__ = "equipquery"
    post_type = "equipquery"
    data: Optional[dict]
    '''
    装备数据，是一个字典
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.echo = all_data.get('echo')
        self.msg_success = all_data.get('msg')
        self.data = all_data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1025


class IndicatorQueryEvent(SendEvent):
    '''
    返回战绩查询结果
    '''
    __event__ = "indicator"
    post_type = "indicator"
    role_info: Optional[dict]
    '''
    角色信息
    '''
    role_performance: Optional[dict]
    '''
    总览数据
    '''
    role_history: Optional[list[dict]]
    '''
    近期记录
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.echo = all_data.get('echo')
        self.msg_success = all_data.get('msg')
        data = all_data.get('data')
        if data is not None:
            self.role_info = data.get('role_info')
            self.role_performance = data.get('role_performance')
            self.role_history = data.get('role_history')

    @classmethod
    def get_api_type(cls):
        return 1026


class AwesomeQueryEvent(SendEvent):
    '''
    返回名剑排行结果
    '''
    __event__ = "awesomequery"
    post_type = "awesomequery"
    data: Optional[dict]
    '''
    排行数据，是一个字典
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.echo = all_data.get('echo')
        self.msg_success = all_data.get('msg')
        self.data = all_data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1027


class TeamCdListEvent(SendEvent):
    '''
    返回团本记录查询结果
    '''
    __event__ = "teamcdlist"
    post_type = "teamcdlist"
    data: Optional[dict]
    '''
    记录数据，是一个字典
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.echo = all_data.get('echo')
        self.msg_success = all_data.get('msg')
        self.data = all_data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1029


Jx3EventType = Union[
    None,
    OpenServerRecvEvent,
    NewsRecvEvent,
    AdventureRecvEvent,
    EquipQueryEvent,
    IndicatorQueryEvent,
    AwesomeQueryEvent,
    TeamCdListEvent
]

Jx3EventList = [
    OpenServerRecvEvent,
    NewsRecvEvent,
    AdventureRecvEvent,
    EquipQueryEvent,
    IndicatorQueryEvent,
    AwesomeQueryEvent,
    TeamCdListEvent
]
