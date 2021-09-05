from configs.config import DEFAULT_SERVER, DEFAULT_STATUS, ROBOT_ACTIVE
from typing import Optional
from tortoise.models import Model
from tortoise import fields


class GroupInfo(Model):
    '''
    QQ群表
    '''
    group_id = fields.IntField(pk=True)
    '''
    QQ群号
    '''
    sign_nums = fields.IntField(default=0)
    '''
    签到次数
    '''
    server = fields.CharField(max_length=255, default=DEFAULT_SERVER)
    '''
    绑定服务器
    '''
    robot_status = fields.BooleanField(default=DEFAULT_STATUS)
    '''
    机器人状态
    '''
    active = fields.IntField(default=ROBOT_ACTIVE)

    class Meta:
        table = "group_info"
        table_description = "管理QQ群信息"

    @classmethod
    async def get_group_list(cls) -> list[int]:
        '''
        返回群列表，开启机器人的
        '''
        record: list[GroupInfo] = await cls.all()
        group_list = []
        for one in record:
            if one.robot_status:
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
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        return record.sign_nums

    @classmethod
    async def get_robot_status(cls, group_id: int) -> Optional[bool]:
        '''
        :说明
            获取机器人开关

        :参数
            * group_id：QQ群号

        :返回
            * bool
        '''
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        return None if record is None else record.robot_status

    @classmethod
    async def reset_sign(cls) -> None:
        '''
        :说明
            重置签到人数
        '''
        await cls.all().update(sign_nums=0)

    @classmethod
    async def sign_in_add(cls, group_id: int) -> None:
        '''
        :说明
            增加群签到人数

        :参数
            * group_id：QQ群号
        '''
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        if record is not None:
            record.sign_nums += 1
            await record.save(update_fields=["sign_nums"])
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
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        if record is not None:
            record.robot_status = status
            await record.save(update_fields=["robot_status"])
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
        await cls.get_or_create(group_id=group_id)

    @classmethod
    async def check_group_init(cls, group_id: int) -> bool:
        '''
        检查群是否注册
        '''
        record = await cls.get_or_none(group_id=group_id)
        return (record is not None)

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
        record = await cls.get_or_none(group_id=group_id)
        return None if record is None else record.server

    @classmethod
    async def set_server(cls, group_id: int, server: str) -> None:
        '''
        :说明
            设置群绑定服务器

        :参数
            * group_id：QQ群号
            * server：服务器名
        '''
        record = await cls.get_or_none(group_id=group_id)
        if record is not None:
            record.server = server
            await record.save(update_fields=["server"])
        else:
            raise Exception

    @classmethod
    async def set_active(cls, group_id: int, active: int) -> None:
        '''
        :说明
            设置群机器人的活跃度

        :参数
            * group_id：QQ群号
            * active：活跃度，1-100
        '''
        record = await cls.get_or_none(group_id=group_id)
        if record is not None:
            record.active = active
            await record.save(update_fields=["active"])
        else:
            raise Exception

    @classmethod
    async def get_active(cls, group_id: int) -> Optional[int]:
        '''
        :说明
            获取机器人活跃度

        :参数
            * group_id：QQ群号

        :返回
            * int：活跃度，1-100
        '''
        record = await cls.get_or_none(group_id=group_id)
        return None if record is None else record.active

    @classmethod
    async def delete_one(cls, group_id: int) -> None:
        '''删除一条数据'''
        record = await cls.get_or_none(group_id=group_id)
        if record is not None:
            await record.delete()
