from time import time
from typing import Optional

from tortoise import fields
from tortoise.models import Model


class SearchRecord(Model):
    '''查询使用记录表'''

    id = fields.IntField(pk=True, generated=True)
    bot_id = fields.IntField()
    '''机器人QQ'''
    group_id = fields.IntField()
    '''群号'''
    app_name = fields.CharField(max_length=255)
    '''查询类型'''
    count = fields.IntField(default=0)
    '''查询次数'''
    last_time = fields.IntField(default=0)
    '''上次查询时间'''

    class Meta:
        table = "search_record"
        table_description = "记录查询次数"

    @classmethod
    async def append_or_update(cls, bot_id: int, group_id: int, app_name: str) -> bool:
        '''增加或更新一条记录'''
        _, flag = await cls.get_or_create(bot_id=bot_id, group_id=group_id, app_name=app_name)
        return flag

    @classmethod
    async def count_search(cls, bot_id: int, group_id: int, app_name: str):
        '''使用一次'''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id, app_name=app_name)
        if record:
            record.count += 1
            record.last_time = int(time())
            await record.save(update_fields=["count", "last_time"])

    @classmethod
    async def get_last_time(cls, bot_id: int, group_id: int, app_name: str) -> Optional[int]:
        '''获取上次使用时间'''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id, app_name=app_name)
        return record.last_time if record else None

    @classmethod
    async def get_count(cls, bot_id: int, group_id: int, app_name: str) -> Optional[int]:
        '''获取统计次数'''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id, app_name=app_name)
        return record.count if record else None

    @classmethod
    async def detele_bot(cls, bot_id: int):
        '''清理一个机器人的数据'''
        await cls.filter(bot_id=bot_id).delete()
