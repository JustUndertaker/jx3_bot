from configs.pathConfig import DATABASE_PATH
from peewee import (
    SqliteDatabase,
    Model,
    IntegerField
)

'''
UserLevel表，用于管理用户权限等级
'''

DB = SqliteDatabase(DATABASE_PATH)


class UserLevel(Model):

    # 表的结构
    user_id = IntegerField(verbose_name='用户QQ号', null=False)
    group_id = IntegerField(verbose_name='QQ群号', null=False)
    UserLevel = IntegerField(verbose_name='权限等级', default=0)

    class Meta:
        table_name = 'user_level'
        database = DB

    @classmethod
    async def get_uer_level(cls, user_id: int, group_id: int) -> int:
        '''
        :说明
            获取权限等级，如果没有则返回None

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * int：权限等级
            * None：
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            return record.UserLevel
        else:
            return None

    @classmethod
    async def set_level(cls, user_id: int, group_id: int, level: int) -> None:
        '''
        :说明
            设置权限，如果没有则创建记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * level：权限等级
        '''
        record, _ = cls.get_or_create(user_id=user_id, group_id=group_id)
        record.UserLevel = level
        record.save()

    @classmethod
    async def delete_one(cls, user_id: int, group_id: int) -> None:
        '''
        :说明
            删除一条记录，不存在则不操作

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        record = cls.get_or_none(cls.user_id == user_id, cls.group_id == group_id)
        if record is not None:
            record.delete_instance()
