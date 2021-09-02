from configs.pathConfig import DATABASE_PATH
from typing import Optional
from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    BooleanField,
    CharField
)


'''
GroupInfo表，用于管理整体用户数据
'''

DB = SqliteDatabase(DATABASE_PATH)


class GroupInfo(Model):

    # 表的结构
    group_id = IntegerField(primary_key=True, verbose_name='QQ群号', null=False)
    sign_nums = IntegerField(verbose_name='当天签到人数', default=0)
    server = CharField(verbose_name='绑定服务器', default='幽月轮')
    robot_status = BooleanField(verbose_name='机器人开关', default=True)

    class Meta:
        table_name = 'group_info'
        database = DB

    @classmethod
    async def get_group_list(cls) -> list:
        '''
        返回群列表
        '''
        record = cls.select()
        group_list = []
        for one in record:
            group_list.append(one.group_id)
        return group_list

    @classmethod
    async def get_sign_nums(cls, group_id: int) -> int:
        '''
        :说明
            获取签到人数，没有实例则创建实例

        :参数
            * group_id：QQ群号

        :返回
            * int：签到人数
        '''
        record, _ = cls.get_or_create(group_id=group_id)
        return record.sign_nums

    @classmethod
    async def get_robot_status(cls, group_id: int) -> Optional[bool]:
        '''
        :说明
            获取机器人开关

        :参数
            * group_id：QQ群号

        :返回
            * int：签到人数
            * None：未找到记录
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        if record is not None:
            return record.robot_status
        else:
            return None

    @classmethod
    async def reset_sign(cls) -> None:
        '''
        :说明
            重置签到人数
        '''
        record_list = cls.select()
        for record in record_list:
            record.sign_nums = 0
            record.save()

    @classmethod
    async def sign_in_add(cls, group_id: int) -> None:
        '''
        :说明
            增加群签到人数

        :参数
            * group_id：QQ群号
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        if record is not None:
            record.sign_nums += 1
            record.save()
        else:
            raise Exception

    @classmethod
    async def set_robot_status(cls, group_id: int, status: bool) -> None:
        '''
        :说明
            设置机器人状态

        :参数
            * group_id：QQ群号
            * status：机器人状态
        '''
        record = cls.get_or_none(group_id=group_id)
        if record is not None:
            record.robot_status = status
            record.save()
        else:
            raise Exception

    @classmethod
    async def append_or_update(cls, group_id: int) -> None:
        '''
        :说明
            * 增加，或者更新一条数据

        :参数
            * group_id：QQ群号
        '''
        cls.get_or_create(group_id=group_id)

    @classmethod
    async def delete_one(cls, group_id: int) -> None:
        '''
        :说明
            删除一条记录

        :参数
            * group_id：QQ群号
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        if record is not None:
            record.delete_instance()

    @classmethod
    async def check_group_init(cls, group_id: int) -> bool:
        '''
        检查群是否注册
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        return record is not None

    @classmethod
    async def get_server(cls, group_id: int) -> Optional[str]:
        '''
        :说明
            查询群绑定服务器

        :参数
            * group_id：QQ群号

        :返回
            * str：服务器名
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        if record is not None:
            return record.server
        else:
            return None

    @classmethod
    async def set_server(cls, group_id: int, server: str) -> None:
        '''
        :说明
            设置群绑定服务器

        :参数
            * group_id：QQ群号
            * server：服务器名
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        if record is not None:
            record.server = server
            record.save()
        else:
            raise Exception
