from typing import Optional

from src.utils.config import config as baseconfig
from tortoise import fields
from tortoise.models import Model

config = baseconfig.get('default')
default_server: str = config.get('server')
robot_status: bool = config.get('robot-status')
robot_active: int = config.get('robot-active')
robot_welcome_status: bool = config.get('robot-welcome-status')
robot_welcome: str = config.get('robot-welcome')
robot_someone_left_status: bool = config.get('robot-someone-left-status')
robot_someone_left: str = config.get('robot-someone-left')
robot_goodnight_status: bool = config.get('robot-goodnight-status')
robot_goodnight: str = config.get('robot-goodnight')


class GroupInfo(Model):
    '''
    QQ群表
    '''
    id = fields.IntField(pk=True, generated=True)
    bot_id = fields.IntField()
    '''机器人QQ'''
    group_id = fields.IntField()
    '''QQ群号'''
    group_name = fields.CharField(max_length=255, default='')
    '''群名'''
    sign_nums = fields.IntField(default=0)
    '''签到次数'''
    server = fields.CharField(max_length=255, default=default_server)
    '''绑定服务器'''
    robot_status = fields.BooleanField(default=robot_status)
    '''机器人状态'''
    active = fields.IntField(default=robot_active)
    '''活跃值'''
    welcome_status = fields.BooleanField(default=robot_welcome_status)
    '''进群通知开关'''
    welcome_text = fields.CharField(max_length=255, default=robot_welcome)
    '''进群通知内容'''
    someoneleft_status = fields.BooleanField(default=robot_someone_left_status)
    '''离群通知开关'''
    someoneleft_text = fields.CharField(max_length=255, default=robot_someone_left)
    '''离群通知内容'''
    goodnight_status = fields.BooleanField(default=robot_goodnight_status)
    '''晚安通知开关'''
    goodnight_text = fields.CharField(max_length=255, default=robot_goodnight)
    '''晚安通知内容'''

    class Meta:
        table = "group_info"
        table_description = "管理QQ群信息"

    @classmethod
    async def get_group_list(cls, bot_id: int) -> list[int]:
        '''
        :说明
            返回群列表，开启机器人的

        :参数
            * bot_id：机器人QQ号
        '''
        record = await cls.filter(bot_id=bot_id)
        group_list = []
        for one in record:
            if one.robot_status:
                group_list.append(one.group_id)
        return group_list

    @classmethod
    async def get_group_name(cls, bot_id: int, group_id: int) -> Optional[str]:
        '''
        :说明
            * 获取群名

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回
            * str：群名
        '''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.group_name

    @classmethod
    async def get_sign_nums(cls, bot_id: int, group_id: int) -> int:
        '''
        :说明
            获取签到人数

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回
            * int：签到人数
        '''
        record: GroupInfo = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.sign_nums

    @classmethod
    async def get_robot_status(cls, bot_id: int, group_id: int) -> Optional[bool]:
        '''
        :说明
            获取机器人开关

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回
            * bool
        '''
        record: GroupInfo = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.robot_status

    @classmethod
    async def reset_sign(cls, bot_id: int) -> None:
        '''
        :说明
            重置签到人数

        :参数
            * bot_id：机器人QQ
        '''
        await cls.filter(bot_id=bot_id).update(sign_nums=0)

    @classmethod
    async def sign_in_add(cls, bot_id: int, group_id: int) -> bool:
        '''
        :说明
            增加群签到人数

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回
            * bool：是否成功
        '''
        record: GroupInfo = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.sign_nums += 1
            await record.save(update_fields=["sign_nums"])
            return True
        else:
            return False

    @classmethod
    async def set_robot_status(cls, bot_id: int, group_id: int, status: bool) -> bool:
        '''
        :说明
            设置机器人状态

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号
            * status：机器人状态

        :返回
            * bool:是否成功
        '''
        record: GroupInfo = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.robot_status = status
            await record.save(update_fields=["robot_status"])
            return True
        else:
            return False

    @classmethod
    async def append_or_update(cls, bot_id: int, group_id: int, group_name: str) -> None:
        '''
        :说明
            * 增加，或者更新一条数据

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号
        '''
        record, _ = await cls.get_or_create(bot_id=bot_id, group_id=group_id)
        record.group_name = group_name
        await record.save(update_fields=["group_name"])

    @classmethod
    async def check_group_init(cls, bot_id: int, group_id: int) -> bool:
        '''
        检查群是否注册
        '''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return (record is not None)

    @classmethod
    async def get_server(cls, bot_id: int, group_id: int) -> Optional[str]:
        '''
        :说明
            查询群绑定服务器

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回
            * str：服务器名
        '''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.server

    @classmethod
    async def set_server(cls, bot_id: int, group_id: int, server: str) -> None:
        '''
        :说明
            设置群绑定服务器

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号
            * server：服务器名
        '''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.server = server
            await record.save(update_fields=["server"])
        else:
            raise Exception

    @classmethod
    async def set_active(cls, bot_id: int, group_id: int, active: int) -> None:
        '''
        :说明
            设置群机器人的活跃度

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号
            * active：活跃度，1-100
        '''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.active = active
            await record.save(update_fields=["active"])
        else:
            raise Exception

    @classmethod
    async def get_active(cls, bot_id: int, group_id: int) -> Optional[int]:
        '''
        :说明
            获取机器人活跃度

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回
            * int：活跃度，1-100
        '''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.active

    @classmethod
    async def set_welcome_status(cls, bot_id: int, group_id: int, welcome_status: bool):
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.welcome_status = welcome_status
            await record.save(update_fields=["welcome_status"])
        else:
            raise Exception

    @classmethod
    async def get_welcome_status(cls, bot_id: int, group_id: int) -> Optional[bool]:
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.welcome_status

    @classmethod
    async def set_welcome_text(cls, bot_id: int, group_id: int, welcome_text: str):
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.welcome_text = welcome_text
            await record.save(update_fields=["welcome_text"])
        else:
            raise Exception

    @classmethod
    async def get_welcome_text(cls, bot_id: int, group_id: int) -> Optional[str]:
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.welcome_text

    @classmethod
    async def set_someoneleft_status(cls, bot_id: int, group_id: int, someoneleft_status: bool):
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.someoneleft_status = someoneleft_status
            await record.save(update_fields=["someoneleft_status"])
        else:
            raise Exception

    @classmethod
    async def get_someoneleft_status(cls, bot_id: int, group_id: int) -> Optional[bool]:
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.someoneleft_status

    @classmethod
    async def set_someoneleft_text(cls, bot_id: int, group_id: int, someoneleft_text: str):
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.someoneleft_text = someoneleft_text
            await record.save(update_fields=["someoneleft_text"])
        else:
            raise Exception

    @classmethod
    async def get_someoneleft_text(cls, bot_id: int, group_id: int) -> Optional[str]:
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.someoneleft_text

    @classmethod
    async def set_goodnight_status(cls, bot_id: int, group_id: int, goodnight_status: bool):
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.goodnight_status = goodnight_status
            await record.save(update_fields=["goodnight_status"])
        else:
            raise Exception

    @classmethod
    async def get_goodnight_status(cls, bot_id: int, group_id: int) -> Optional[bool]:
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.goodnight_status

    @classmethod
    async def set_goodnight_text(cls, bot_id: int, group_id: int, goodnight_text: str):
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            record.goodnight_text = goodnight_text
            await record.save(update_fields=["goodnight_text"])
        else:
            raise Exception

    @classmethod
    async def get_goodnight_text(cls, bot_id: int, group_id: int) -> Optional[str]:
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        return None if record is None else record.goodnight_text

    @classmethod
    async def get_all_data(cls, bot_id: int) -> list[dict]:
        '''
        :返回所有数据,dict字段：
        * group_id：群号
        * group_name：群名
        * sign_nums：签到数
        * server：服务器名
        * robot_status：运行状态
        * active：活跃值
        '''
        record_list = await cls.filter(bot_id=bot_id)
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
    async def change_status_all(cls, bot_id: int, status: bool) -> None:
        '''
        改变所有群开关
        '''
        await cls.filter(bot_id=bot_id).update(robot_status=status)

    @classmethod
    async def delete_one(cls, bot_id: int, group_id: int) -> bool:
        '''删除一条数据'''
        record = await cls.get_or_none(bot_id=bot_id, group_id=group_id)
        if record is not None:
            await record.delete()
            return True
        return False

    @classmethod
    async def detele_bot(cls, bot_id: int) -> None:
        '''删除一个机器人的数据'''
        await cls.filter(bot_id=bot_id).delete()
