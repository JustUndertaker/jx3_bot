import random

from tortoise import fields
from tortoise.models import Model


class TokenInfo(Model):
    '''存储token表'''
    id = fields.IntField(pk=True, generated=True)
    bot_id = fields.IntField()
    '''机器人QQ'''
    token = fields.CharField(max_length=255)
    '''token值'''
    alive = fields.BooleanField(null=True, default=True)
    '''存活'''

    class Meta:
        table = "token_info"
        table_description = "存储token用"

    @classmethod
    async def get_token(cls, bot_id: int) -> list[dict]:
        '''
        :说明
            获取token列表，返回[]

        :参数
            * bot_id：机器人QQ

        :返回
            * list[dict]，dict{"token":"","alive":""}
        '''
        record = await cls.filter(bot_id=bot_id).values("token", "alive")
        return record

    @classmethod
    async def get_alive_token(cls, bot_id: int) -> list[str]:
        '''
        :说明
            获取可用的token列表，返回[]

        :参数
            * bot_id：机器人QQ

        :返回
            * list[str]
        '''
        record = await cls.filter(bot_id=bot_id, alive=True).values("token")
        req_list = [one['token'] for one in record]
        random.shuffle(req_list)
        return req_list

    @classmethod
    async def change_alive(cls, bot_id: int, token: str, alive: bool):
        '''改变token的有效性'''
        record = await cls.get_or_none(bot_id=bot_id, token=token)
        if record is not None:
            record.alive = alive
            await record.save(update_fields=["alive"])

    @classmethod
    async def append_token(cls, bot_id: int, token: str) -> bool:
        '''
        :说明
            增加一条token

        :参数
            * bot_id：机器人QQ
            * token：token值

        :返回
            * bool：是否是新token
        '''
        _, flag = await cls.get_or_create(bot_id=bot_id, token=token)
        return flag

    @classmethod
    async def remove_token(cls, bot_id: int, token: str) -> bool:
        '''
        :说明
            删除一条token

        :参数
            * bot_id：机器人QQ
            * token：token值

        :返回
            * bool：是否成功删除
        '''
        record = await cls.get_or_none(bot_id=bot_id, token=token)
        if record is None:
            return False

        await record.delete()
        return True

    @classmethod
    async def detele_bot(cls, bot_id: int):
        '''
        :说明
            删除一个bot的token

        :参数
            * bot_id：机器人QQ
        '''
        await cls.filter(bot_id=bot_id).delete()
