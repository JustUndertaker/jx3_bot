from configs.pathConfig import DATABASE_PATH
from tortoise import Tortoise

from .log import logger


async def database_init():
    '''
    初始化建表
    '''
    logger.debug('正在注册数据库')
    db_url = f'sqlite://{DATABASE_PATH}'
    # 这里填要加载的表
    models = [
        'modules.group_info',
        'modules.plugin_info',
        'modules.user_info'
    ]
    modules = {"models": models}
    await Tortoise.init(db_url=db_url, modules=modules)
    await Tortoise.generate_schemas()
    logger.debug('数据库注册完成')
