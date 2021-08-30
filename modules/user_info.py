from datetime import date

from configs.pathConfig import DATABASE_PATH
from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    CharField,
    DateField
)

'''
UserInfo表，用于管理整体用户数据
'''

DB = SqliteDatabase(DATABASE_PATH)


class UserInfo(Model):

    # 表的结构
    user_id = IntegerField(verbose_name='用户QQ号', null=False)
    group_id = IntegerField(verbose_name='QQ群号', null=False)
    user_name = CharField(verbose_name='用户昵称', default='')
    gold = IntegerField(verbose_name='金币数', default=0)
    friendly = IntegerField(verbose_name='好感度', default=0)
    lucky = IntegerField(verbose_name='今日运势', default=0)
    sign_times = IntegerField(verbose_name='累计签到次数', default=0)
    last_sign = DateField(verbose_name='上次签到日期', null=True)

    class Meta:
        table_name = 'user_info'
        database = DB

    def display(self):
        t = f'QQ号: {self.user_id}\n' \
            f'金币: {self.gold}\n' \
            f'好感度: {self.friendly}\n' \
            f'今日运势: {self.lucky}\n' \
            f'累计签到: {self.sign_times}\n'
        if self.last_sign is not None:
            t += f'上次签到: {self.last_sign}'
        return t

    @classmethod
    async def user_display(cls, user_id: int, group_id: int):
        '''
        :说明：
            获取用户

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * UserInfo：用户数据记录
            * None：不存在记录
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.display()
        else:
            return ''

    @classmethod
    async def get_friendly(cls, user_id: int, group_id: int) -> int:
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
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.friendly
        else:
            return None

    @classmethod
    async def get_gold(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取用户的金币

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * 好感度
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.gold
        else:
            return None

    @classmethod
    async def get_sign_times(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取累计签到次数

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * int：累计签到次数
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.sign_times
        else:
            return None

    @classmethod
    async def get_last_sign(cls, user_id: int, group_id: int) -> date:
        '''
        :说明：
            获取用户的上次签到日期

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * date:上次签到日期
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.last_sign
        else:
            return None

    @classmethod
    async def get_lucky(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取用户的运势

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * int：今日运势
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.lucky
        else:
            return None

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
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            record.last_sign = today
            record.sign_times += 1
            record.save()
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
        record, _ = cls.get_or_create(user_id=user_id, group_id=group_id)
        record.user_name = user_name
        record.save()

    @classmethod
    async def delete_one(cls, user_id: int, group_id: int) -> None:
        '''
        :说明
            删除一条记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            record.delete_instance()

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
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            record.lucky = lucky
            record.save()
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
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            record.gold += num
            record.save()
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
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            record.friendly += num
            record.save()
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
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        return (record is not None)
