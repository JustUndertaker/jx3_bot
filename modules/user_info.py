from datetime import date
from typing import Optional
from tortoise.models import Model
from tortoise import fields


class UserInfo(Model):
    '''
    用户表
    '''
    id = fields.IntField(pk=True, generated=True)
    user_id = fields.IntField()
    '''
    用户QQ号
    '''
    group_id = fields.IntField()
    '''
    所属QQ群号
    '''
    user_name = fields.CharField(max_length=255, default="")
    '''
    用户昵称
    '''
    gold = fields.IntField(default=0)
    '''
    用户金币
    '''
    friendly = fields.IntField(default=0)
    '''
    好感度
    '''
    lucky = fields.IntField(default=1)
    '''
    今日运势
    '''
    sign_times = fields.IntField(default=0)
    '''
    累计签到次数
    '''
    last_sign = fields.DateField(null=True)

    class Meta:
        table = "user_info"
        table_description = "管理用户"

    @classmethod
    async def get_friendly(cls, user_id: int, group_id: int) -> Optional[int]:
        '''
        :说明：
            获取用户的好感度

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * int：好感度
            * None：不存在记录
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        return None if record is None else record.friendly

    @classmethod
    async def get_gold(cls, user_id: int, group_id: int) -> Optional[int]:
        '''
        :说明：
            获取用户的金币

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * 好感度
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        return None if record is None else record.gold

    @classmethod
    async def get_sign_times(cls, user_id: int, group_id: int) -> Optional[int]:
        '''
        :说明：
            获取累计签到次数

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * int：累计签到次数
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        return None if record is None else record.sign_times

    @classmethod
    async def get_last_sign(cls, user_id: int, group_id: int) -> Optional[date]:
        '''
        :说明：
            获取用户的上次签到日期

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * date:上次签到日期
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        return None if record is None else record.last_sign

    @classmethod
    async def get_lucky(cls, user_id: int, group_id: int) -> Optional[int]:
        '''
        :说明：
            获取用户的运势

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * int：今日运势
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        return None if record is None else record.lucky

    @classmethod
    async def sign_in(cls, user_id: int, group_id: int) -> None:
        '''
        :说明：
            签到，更新签到日期，增加签到次数

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        today = date.today()
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        if record is not None:
            record.last_sign = today
            record.sign_times += 1
            await record.save(update_fields=["last_sign", "sign_times"])
        else:
            raise Exception

    @classmethod
    async def append_or_update(cls, user_id: int, group_id: int, user_name: str) -> None:
        '''
        :说明
            增加，或者更新一条数据

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * user_name：用户昵称
        '''
        record, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        record.user_name = user_name
        await record.save(update_fields=["user_name"])

    @classmethod
    async def delete_one(cls, user_id: int, group_id: int) -> None:
        '''
        :说明
            删除一条记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        if record is not None:
            await record.delete()

    @classmethod
    async def change_lucky(cls, user_id: int, group_id: int, lucky: int) -> None:
        '''
        :说明
            改变运势

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * lucky：运势值
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        if record is not None:
            record.lucky = lucky
            await record.save(update_fields=["lucky"])
        else:
            raise Exception

    @classmethod
    async def change_gold(cls, user_id: int, group_id: int, num: int) -> None:
        '''
        :说明
            改变金币数量

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * num：改变金币数量
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        if record is not None:
            record.gold += num
            await record.save(update_fields=['gold'])
        else:
            raise Exception

    @classmethod
    async def change_friendly(cls, user_id: int, group_id: int, num: int) -> None:
        '''
        :说明
            改变友好度

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * num：改变友好度
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        if record is not None:
            record.friendly += num
            await record.save(update_fields=['friendly'])
        else:
            raise Exception

    @classmethod
    async def exist(cls, user_id: int, group_id: int) -> bool:
        '''
        :说明
            判断是否存在该记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * bool：是否存在
        '''
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        return (record is not None)
