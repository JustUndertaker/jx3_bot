from typing import Optional

from tortoise import fields
from tortoise.models import Model


class PluginInfo(Model):
    '''
    插件管理表
    '''
    id = fields.IntField(pk=True, generated=True)
    bot_id = fields.IntField()
    '''
    机器人QQ
    '''
    module_name = fields.CharField(max_length=255)
    '''
    插件名称
    '''
    description = fields.CharField(max_length=255, default='')
    '''
    插件描述
    '''
    group_id = fields.IntField()
    '''
    QQ群号
    '''
    status = fields.BooleanField(default=True)
    '''
    插件状态
    '''

    class Meta:
        table = "plugin_info"
        table_description = "处理插件"

    @classmethod
    async def get_status(cls, bot_id: int, module_name: str, group_id: int) -> Optional[bool]:
        '''
        :说明
            返回插件开关

        :参数
            * bot_id：机器人QQ
            * module_name：插件模块名称
            * group_id：QQ群号

        :返回
            * bool：当前插件开关状态
        '''
        record = await cls.get_or_none(bot_id=bot_id, module_name=module_name, group_id=group_id)
        return None if record is None else record.status

    @classmethod
    async def change_status(cls, bot_id: int, module_name: str, group_id: int, status: bool) -> None:
        '''
        :说明
            设置插件开启状态

        :参数
            * bot_id：机器人QQ
            * module_name：插件模块名称
            * group_id：QQ群号
            * status：开关状态
        '''
        record = await cls.get_or_none(bot_id=bot_id, module_name=module_name, group_id=group_id)
        if record is not None:
            record.status = status
            await record.save(update_fields=["status"])
        else:
            raise Exception

    @classmethod
    async def append_or_update(cls, bot_id: int, module_name: str, description: str,  group_id: int) -> None:
        '''
        :说明
            增加，或更新一条数据

        :参数
            * bot_id：机器人QQ
            * module_name：插件模块名
            * description：插件描述
            * group_id：QQ群号
        '''
        record, _ = await cls.get_or_create(bot_id=bot_id, module_name=module_name, group_id=group_id)
        record.description = description
        await record.save(update_fields=["description"])

    @classmethod
    async def set_group_status(cls, bot_id: int, group_id: int, status: bool) -> None:
        '''
        :说明
            设置某个群所有插件状态

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号
            * status：插件状态
        '''
        await cls.filter(bot_id=bot_id, group_id=group_id).update(status=status)

    @classmethod
    async def set_module_status(cls, bot_id: int, module_name: str, status: bool) -> None:
        '''
        :说明
            设置某个插件全局状态

        :参数
            * bot_id：机器人QQ
            * module_name：插件模块名
            * status：插件状态
        '''
        await cls.filter(bot_id=bot_id, module_name=module_name).update(status=status)

    @classmethod
    async def get_all_status_from_group(cls, bot_id: int, group_id: int) -> list[dict]:
        '''
        :说明
            返回某个群的所有插件状态

        :参数
            * bot_id：机器人QQ
            * group_id：QQ群号

        :返回

            * list[dict]：dict字段：module_name，description，status
        '''
        req = await cls.filter(bot_id=bot_id, group_id=group_id).order_by("module_name").values("module_name", "description", "status")
        return req

    @classmethod
    async def deltele_group(cls, bot_id: int, group_id: int) -> None:
        '''删除一个群插件'''
        await cls.filter(bot_id=bot_id, group_id=group_id).delete()

    @classmethod
    async def detele_bot(cls, bot_id: int) -> None:
        '''删除一个机器人'''
        await cls.filter(bot_id=bot_id).delete()
