from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.adapters.cqhttp.message import Message


class Event(BaseEvent):

    __event__ = ""
    data: dict
    post_type: str = ""

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.post_type

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


class OpenServerEvent(Event):
    '''
    开服提醒事件
    '''
    __event__ = "OpenServer"
    post_type = "OpenServer"
    data: dict = {}

    def set_event_data(self, data: dict):
        self.data = data


class NewsEvent(Event):
    '''
    官方新闻推送事件
    '''
    __event__ = "news"
    post_type = "news"
    data: dict = {}

    def set_event_data(self, data: dict):
        self.data = data


class AdventureEvent(Event):
    '''
    奇遇播报事件
    '''
    __event__ = "adventure"
    post_type = "adventure"
    data: dict = {}

    def set_event_data(self, data: dict):
        self.data = data
