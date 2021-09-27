from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.models import Model


class BotInfo(Model):
    '''QQ机器人表'''
    bot_id = fields.IntField(pk=True)
    '''机器人QQ号'''
    owner_id = fields.IntField(null=True)
    '''管理员账号'''
    last_sign = fields.DatetimeField(null=True)
    '''上次登录时间'''
    last_left = fields.DatetimeField(null=True)
    '''上次离线时间'''
    online = fields.BooleanField(default=True)
    '''当前在线情况'''

    class Meta:
        table = "bot_info"
        table_description = "管理QQ机器人账号信息"

    @classmethod
    async def bot_connect(cls, bot_id):
        '''
        :说明
            机器人链接

        :参数
            * bot_id：机器人QQ号
        '''
        record, _ = await cls.get_or_create(bot_id=bot_id)
        now_time = datetime.now()
        record.last_sign = now_time
        record.online = True
        await record.save(update_fields=["last_sign", "online"])

    @classmethod
    async def bot_disconnect(cls, bot_id):
        '''
        :说明
            机器人断开链接

        :参数
            * bot_id：机器人QQ号
        '''
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            now_time = datetime.now()
            record.last_left = now_time
            record.online = False
            await record.save(update_fields=["last_left", "online"])

    @classmethod
    async def bot_shoutdown(cls):
        '''关闭所有机器人链接'''
        now_time = datetime.now()
        await cls.all().update(last_left=now_time, online=False)

    @classmethod
    async def set_owner(cls, bot_id, owner_id):
        '''
        :说明
            设置机器人管理员

        :参数
            * bot_id：机器人QQ号
            * owner_id：管理员QQ号
        '''
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            record.owner_id = owner_id
            await record.save(update_fields=["owner_id"])

    @classmethod
    async def get_owner(cls, bot_id) -> Optional[int]:
        '''
        :说明
            获取机器人管理员

        :参数
            * bot_id：机器人QQ

        :返回
            * int：管理员QQ
            * None
        '''
        record = await cls.get_or_none(bot_id=bot_id)
        owner_id = None
        if record is not None:
            owner_id = record.owner_id
        return owner_id

    @classmethod
    async def get_online(cls, bot_id) -> Optional[bool]:
        '''
        :说明
            获取机器人在线状态

        :参数
            * bot_id：机器人QQ

        :返回
            * bool：是否在线
            * None：不存在
        '''
        record = await cls.get_or_none(bot_id=bot_id)
        online = None
        if record is not None:
            online = record.online
        return online

    @classmethod
    async def detele_bot(cls, bot_id) -> bool:
        '''
        :说明
            删除机器人

        :参数
            * bot_id：机器人QQ

        :返回
            * bool：删除是否成功，失败则数据不存在
        '''
        record = await cls.get_or_none(bot_id=bot_id)
        if record is not None:
            await record.delete()
            return True
        return False

    @classmethod
    async def get_disconnect_bot(cls) -> list[dict]:
        '''
        获取离线bot列表,dict["bot_id", "last_left"]
        '''
        record_list = await cls.filter(online=False).values("bot_id", "last_left")
        return record_list
