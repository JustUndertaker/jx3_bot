from nonebot.log import logger
from tortoise import Tortoise


async def database_init():
    '''
    初始化建表
    '''
    logger.debug('正在注册数据库')
    database_path = "./data/data.db"
    db_url = f'sqlite://{database_path}'
    # 这里填要加载的表
    models = [
        'src.modules.group_info',
        'src.modules.plugin_info',
        'src.modules.user_info'
    ]
    modules = {"models": models}
    await Tortoise.init(db_url=db_url, modules=modules)
    await Tortoise.generate_schemas()
    logger.debug('数据库注册完成')
