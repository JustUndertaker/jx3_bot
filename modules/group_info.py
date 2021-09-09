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
    group_name = fields.CharField(max_length=255, default='')
    '''
    群名
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
    async def get_group_name(cls, group_id: int) -> Optional[str]:
        '''
        :说明
            * 获取群名

        :参数
            * group_id：QQ群号

        :返回
            * str：群名
        '''
        record = await cls.get_or_none(group_id=group_id)
        return None if record is None else record.group_name

    @classmethod
    async def get_sign_nums(cls, group_id: int) -> int:
        '''
        :说明
            获取签到人数

        :参数
            * group_id：QQ群号

        :返回
            * int：签到人数
        '''
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        return None if record is None else record.sign_nums

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
    async def sign_in_add(cls, group_id: int) -> bool:
        '''
        :说明
            增加群签到人数

        :参数
            * group_id：QQ群号

        :返回
            * bool：是否成功
        '''
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        if record is not None:
            record.sign_nums += 1
            await record.save(update_fields=["sign_nums"])
            return True
        else:
            return False

    @classmethod
    async def set_robot_status(cls, group_id: int, status: bool) -> bool:
        '''
        :说明
            设置机器人状态

        :参数
            * group_id：QQ群号
            * status：机器人状态

        :返回
            * bool:是否成功
        '''
        record: GroupInfo = await cls.get_or_none(group_id=group_id)
        if record is not None:
            record.robot_status = status
            await record.save(update_fields=["robot_status"])
            return True
        else:
            return False

    @classmethod
    async def append_or_update(cls, group_id: int, group_name: str) -> None:
        '''
        :说明
            * 增加，或者更新一条数据

        :参数
            * group_id：QQ群号
        '''
        record, _ = await cls.get_or_create(group_id=group_id)
        record.group_name = group_name
        await record.save(update_fields=["group_name"])

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
    async def get_all_data(cls) -> list[dict]:
        '''
        :返回所有数据,dict字段：
        * group_id：群号
        * group_name：群名
        * sign_nums：签到数
        * server：服务器名
        * robot_status：运行状态
        * active：活跃值
        '''
        record_list = await cls.all()
        data = []
        for record in record_list:
            one_data = {}
            one_data['group_id'] = record.group_id
            one_data['group_name'] = record.group_name
            one_data['sign_nums'] = record.sign_nums
            one_data['server'] = record.server
            one_data['robot_status'] = record.robot_status
            one_data['active'] = record.active
            data.append(one_data)
        return data

    @classmethod
    async def change_status_all(cls, status: bool) -> None:
        '''改变所有机器人开关'''
        await cls.all().update(robot_status=status)

    @classmethod
    async def delete_one(cls, group_id: int) -> bool:
        '''删除一条数据'''
        record = await cls.get_or_none(group_id=group_id)
        if record is not None:
            await record.delete()
            return True
        return False
