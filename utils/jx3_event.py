from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.adapters.cqhttp.message import Message
from typing import Optional, Union
import time


class WS_ECHO():
    '''
    维护连接池数据
    '''
    echo: int
    '''
    认证echo
    '''
    user_id: Optional[int]
    '''
    私聊消息：QQ号
    '''
    group_id: Optional[int]
    '''
    群消息：QQ群号
    '''

    def __init__(self, echo: int, user_id: Optional[int] = None, group_id: Optional[int] = None):
        self.echo = echo
        self.user_id = user_id
        self.group_id = group_id


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
    echo: Optional[int]
    '''
    认证echo
    '''

    def set_message_type(self, ws_econ: WS_ECHO):
        self.user_id = ws_econ.user_id
        self.group_id = ws_econ.group_id

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
        super(NewsRecvEvent, self).__init__()
        data: dict = all_data.get('data')
        self.news_type = data.get('type')
        self.news_tittle = data.get('title')
        self.news_url = data.get('url')
        self.news_date = data.get('news_date')

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
        super(AdventureRecvEvent, self).__init__()
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


class DailyEvent(SendEvent):
    '''
    返回日常事件
    '''
    __event__ = "daily"
    post_type = "daily"
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
        self.DayWar = data.get('DayWar')
        self.Week = data.get('Week')
        self.DayBattle = data.get('DayBattle')
        self.DayCamp = data.get('DayCamp')
        self.DayCommon = data.get('DayCommon')
        self.DayDraw = data.get('DayDraw')
        self.WeekCommon = data.get('WeekCommon')
        self.WeekFive = data.get('WeekFive')
        self.WeekTeam = data.get('WeekTeam')

    @classmethod
    def get_api_type(cls):
        return 1001


class OpenServerSendEvent(SendEvent):
    '''
    返回开服查询结果
    '''
    __event__ = "open_server_send"
    post_type = "open_server_send"
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
        self.echo = all_data.get('echo')
        data: dict = all_data.get('data')
        self.server = data.get('server')
        self.region = data.get('region')
        status = data.get('status')
        self.status = (True if status == 1 else False)

    @classmethod
    def get_api_type(cls):
        return 1002


class GoldQueryEvent(SendEvent):
    '''
    返回金价查询结果
    '''
    __event__ = "gold_query"
    post_type = "gold_query"
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

    @classmethod
    def get_api_type(cls):
        return 1003


class FlowerPriceEvent(SendEvent):
    '''
    返回鲜花价格查询结果
    '''
    __event__ = "flower_price"
    post_type = "flower_price"
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

    @classmethod
    def get_api_type(cls):
        return 1004


class MatchEquipEvent(SendEvent):
    '''
    返回配装查询结果
    '''
    __event__ = "match_equip"
    post_type = "match_equip"
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

    @classmethod
    def get_api_type(cls):
        return 1006


class MainServerEvent(SendEvent):
    '''
    返回主服务器查询结果
    '''
    __event__ = "main_server"
    post_type = "main_server"
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

    @classmethod
    def get_api_type(cls):
        return 1007


class ExtraPointEvent(SendEvent):
    '''
    返回奇穴查询结果
    '''
    __event__ = "extra_point"
    post_type = "extra_point"
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

    @classmethod
    def get_api_type(cls):
        return 1008


class MedicineEvent(SendEvent):
    '''
    返回小药查询结果
    '''
    __event__ = "medicine"
    post_type = "medicine"
    name: Optional[str]
    '''
    心法名称
    '''
    heightenFood: Optional[str]
    '''
    增强食品
    '''
    auxiliaryFood: Optional[str]
    '''
    辅助食品
    '''
    heightenDrug: Optional[str]
    '''
    增强药品
    '''
    auxiliaryDrug: Optional[str]
    '''
    辅助药品
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(MedicineEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.heightenFood = data.get('heightenFood')
        self.auxiliaryFood = data.get('auxiliaryFood')
        self.heightenDrug = data.get('heightenDrug')
        self.auxiliaryDrug = data.get('auxiliaryDrug')

    @classmethod
    def get_api_type(cls):
        return 1010


class MacroEvent(SendEvent):
    '''
    返回宏查询结果
    '''
    __event__ = "macro"
    post_type = "macro"
    name: Optional[str]
    '''
    心法名称
    '''
    plan: Optional[str]
    '''
    奇穴
    '''
    command: Optional[str]
    '''
    宏命令
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(MacroEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.plan = data.get('plan')
        self.command = data.get('command')

    @classmethod
    def get_api_type(cls):
        return 1011


class ItemPriceEvent(SendEvent):
    '''
    返回物价查询结果
    '''
    __event__ = "itemprice"
    post_type = "itemprice"
    name: Optional[str]
    '''
    物品名称
    '''
    data: Optional[list[dict]]
    '''
    物价数据
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(ItemPriceEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.data = all_data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1012


class AdventureConditionEvent(SendEvent):
    '''
    返回奇遇条件查询结果
    '''
    __event__ = "adventurecondition"
    post_type = "adventurecondition"
    name: Optional[str]
    '''
    奇遇名称
    '''
    method: Optional[str]
    '''
    触发方式
    '''
    need: Optional[str]
    '''
    满足条件
    '''
    other: Optional[str]
    '''
    其他可能
    '''
    reward: Optional[str]
    '''
    物品奖励
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(AdventureConditionEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.method = data.get('method')
        self.need = data.get('need')
        self.other = data.get('other')
        self.reward = data.get('reward')

    @classmethod
    def get_api_type(cls):
        return 1013


class ExamEvent(SendEvent):
    '''
    返回科举查询结果
    '''
    __event__ = "exam"
    post_type = "exam"
    question: Optional[str]
    '''
    科举题目
    '''
    answer: Optional[str]
    '''
    考试答案
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(ExamEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.question = data.get('question')
        self.answer = data.get('answer')

    @classmethod
    def get_api_type(cls):
        return 1014


class FurnitureMapEvent(SendEvent):
    '''
    返回地图器物查询结果
    '''
    __event__ = "furnituremap"
    post_type = "furnituremap"
    data: Optional[list[dict]]
    '''
    家具数据，是一个列表
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(FurnitureMapEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.data = data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1015


class FurnitureEvent(SendEvent):
    '''
    返回装饰查询结果
    '''
    __event__ = "furniture"
    post_type = "furniture"
    name: Optional[str]
    '''
    装饰名称
    '''
    type: Optional[int]
    '''
    装饰类型
    '''
    quality: Optional[int]
    '''
    装饰品质
    '''
    source: Optional[str]
    '''
    装饰来源
    '''
    architecture: Optional[int]
    '''
    装饰价格
    '''
    levelLimit: Optional[int]
    '''
    家园所需等级
    '''
    qualityLevel: Optional[int]
    '''
    品质等级
    '''
    viewScore: Optional[int]
    '''
    观赏等级
    '''
    practicalScore: Optional[int]
    '''
    实用等级
    '''
    hardScore: Optional[int]
    '''
    坚固等级
    '''
    geomanticScore: Optional[int]
    '''
    风水等级
    '''
    interestingScore: Optional[int]
    '''
    趣味等级
    '''
    imagePath: Optional[str]
    '''
    图鉴链接
    '''
    tip: Optional[str]
    '''
    装饰介绍
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(FurnitureEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.type = data.get('type')
        self.quality = data.get('quality')
        self.source = data.get('source')
        self.architecture = data.get('architecture')
        self.levelLimit = data.get('levelLimit')
        self.qualityLevel = data.get('qualityLevel')
        self.viewScore = data.get('viewScore')
        self.practicalScore = data.get('practicalScore')
        self.hardScore = data.get('hardScore')
        self.geomanticScore = data.get('geomanticScore')
        self.interestingScore = data.get('interestingScore')
        self.imagePath = data.get('imagePath')
        self.tip = data.get('tip')

    @classmethod
    def get_api_type(cls):
        return 1016


class AdventureSearchEvent(SendEvent):
    '''
    返回奇遇查询结果
    '''
    __event__ = "adventuresearch"
    post_type = "adventuresearch"
    data: Optional[list[dict]]
    '''
    奇遇数据，是一个列表
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(AdventureSearchEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.data = data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1018


class SaoHuaEvent(SendEvent):
    '''
    返回随机骚话查询结果
    '''
    __event__ = "saohua"
    post_type = "saohua"
    text: Optional[str]
    '''
    骚话内容
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(SaoHuaEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.text = data.get('text')

    @classmethod
    def get_api_type(cls):
        return 1019


class PendantEvent(SendEvent):
    '''
    返回挂件查询结果
    '''
    __event__ = "pendant"
    post_type = "pendant"
    name: Optional[str]
    '''
    挂件名称
    '''
    type: Optional[str]
    '''
    物品类型
    '''
    use: Optional[str]
    '''
    使用特效
    '''
    explain: Optional[str]
    '''
    物品说明
    '''
    obtain: Optional[str]
    '''
    获取方式
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(PendantEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.name = data.get('name')
        self.type = data.get('type')
        self.use = data.get('use')
        self.explain = data.get('explain')
        self.obtain = data.get('obtain')

    @classmethod
    def get_api_type(cls):
        return 1021


class ExperienceEvent(SendEvent):
    '''
    返回资历查询结果
    '''
    __event__ = "experience"
    post_type = "experience"
    data: Optional[list[dict]]
    '''
    资历数据，是一个列表
    '''

    def __init__(self, all_data: dict):
        '''
        重写初始化函数
        '''
        super(ExperienceEvent, self).__init__()
        self.echo = all_data.get('echo')
        data = all_data.get('data')
        self.data = data.get('data')

    @classmethod
    def get_api_type(cls):
        return 1022


Jx3EventType = Union[
    None,
    OpenServerRecvEvent,
    NewsRecvEvent,
    AdventureRecvEvent,
    DailyEvent,
    OpenServerSendEvent,
    GoldQueryEvent,
    FlowerPriceEvent,
    MatchEquipEvent,
    MainServerEvent,
    ExtraPointEvent,
    MedicineEvent,
    MacroEvent,
    ItemPriceEvent,
    AdventureConditionEvent,
    ExamEvent,
    FurnitureMapEvent,
    FurnitureEvent,
    AdventureSearchEvent,
    SaoHuaEvent,
    PendantEvent,
    ExperienceEvent
]

Jx3EventList = [
    OpenServerRecvEvent,
    NewsRecvEvent,
    AdventureRecvEvent,
    DailyEvent,
    OpenServerSendEvent,
    GoldQueryEvent,
    FlowerPriceEvent,
    MatchEquipEvent,
    MainServerEvent,
    ExtraPointEvent,
    MedicineEvent,
    MacroEvent,
    ItemPriceEvent,
    AdventureConditionEvent,
    ExamEvent,
    FurnitureMapEvent,
    FurnitureEvent,
    AdventureSearchEvent,
    SaoHuaEvent,
    PendantEvent,
    ExperienceEvent
]
