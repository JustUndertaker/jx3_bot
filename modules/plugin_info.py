from typing import Union
from configs.pathConfig import DATABASE_PATH
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    BooleanField
)

'''
plugin_info表，用于管理插件开关
'''

DB = SqliteDatabase(DATABASE_PATH)


class PluginInfo(Model):

    # 表的结构
    module_name = CharField(verbose_name='插件模块名称', null=False)
    group_id = IntegerField(verbose_name='QQ群号', null=False)
    status = BooleanField(verbose_name='插件开关状态', null=False, default=True)

    class Meta:
        table_name = 'plugin_info'
        database = DB

    @classmethod
    async def get_status(cls, module_name: str, group_id: int) -> Union[bool, None]:
        '''
        :说明
            返回插件开关

        :参数
            * module_name：插件模块名称
            * group_id：QQ群号

        :返回
            * bool：当前插件开关状态
        '''
        record = cls.get_or_none(cls.module_name == module_name, cls.group_id == group_id)
        if record is not None:
            return record.status
        else:
            return None

    @classmethod
    async def change_status(cls, module_name: str, group_id: int, status: bool) -> None:
        '''
        :说明
            设置插件开启状态

        :参数
            * module_name：插件模块名称
            * group_id：QQ群号
            * status：开关状态
        '''
        record = cls.get_or_none(cls.module_name == module_name, cls.group_id == group_id)
        if record is not None:
            record.status = status
            record.save()
        else:
            raise Exception

    @classmethod
    async def append_or_update(cls, module_name: str, group_id: int) -> None:
        '''
        :说明
            增加，或更新一条数据

        :参数
            * module_name：插件模块名
            * group_id：QQ群号
        '''
        record, is_create = cls.get_or_create(module_name=module_name, group_id=group_id)
        if is_create:
            record.status = True
            record.save()

    @classmethod
    async def set_group_status(cls, group_id: int, status: bool) -> None:
        '''
        :说明
            设置某个群所有插件状态

        :参数
            * group_id：QQ群号
            * status：插件状态
        '''
        record_list = cls.select().where(cls.group_id == group_id)
        for record in record_list:
            record.status = status
            record.save()

    @classmethod
    async def set_module_status(cls, module_name: str, status: bool) -> None:
        '''
        :说明
            设置某个插件全局状态

        :参数
            * module_name：插件模块名
            * status：插件状态
        '''
        record_list = cls.select().where(cls.module_name == module_name)
        for record in record_list:
            record.status = status
            record.save()

    @classmethod
    async def get_all_status_from_group(cls, group_id: int) -> list[dict]:
        '''
        :说明
            返回某个群的所有插件状态

        :参数
            * group_id：QQ群号

        :返回

            * list[dict]：dict字段：module_name，status
        '''
        req = []
        record_list = cls.select().where(cls.group_id == group_id)
        for record in record_list:
            reqdict = {}
            reqdict['module_name'] = record.module_name
            reqdict['status'] = record.status
            req.append(reqdict)
        return req

    @classmethod
    async def check_group_init(cls, group_id: int) -> bool:
        '''
        :说明
            检测群是否注册

        :参数
            * group_id：QQ群号

        :返回
            * bool：是否注册
        '''
        record = cls.get_or_none(cls.group_id == group_id)
        return record is not None
