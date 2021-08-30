from peewee import SqliteDatabase
from configs.pathConfig import DATABASE_PATH
from modules.user_info import UserInfo
from modules.group_info import GroupInfo
from modules.user_level import UserLevel
from modules.plugin_info import PluginInfo

from nonebot.log import logger

from modules.duel_history import DuelHistory


def database_init():
    '''
    初始化建表
    '''
    logger.debug('正在注册数据库')
    table_list = [
        UserInfo,
        GroupInfo,
        UserLevel,
        PluginInfo,
        DuelHistory,
    ]
    DB = SqliteDatabase(DATABASE_PATH)
    DB.connect()
    DB.create_tables(table_list)
    logger.debug('数据库注册完成')
