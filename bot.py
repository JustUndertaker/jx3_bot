#!/usr/bin/python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from src.utils.config import config_init
from src.utils.database import database_init
from src.utils.monkeypatch import monkeypatch
from src.utils.scheduler import start_scheduler

# 注册配置
config_init()
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# 注册数据库
driver.on_startup(database_init)
# 开启定时器
driver.on_startup(start_scheduler)

# 加载管理插件
nonebot.load_plugins("src/managers")
# 加载其他插件
nonebot.load_plugins("src/plugins")
# nonebot.load_plugin("nonebot_plugin_test")


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    monkeypatch()  # 猴子补丁，针对windows平台
    nonebot.run(app="__mp_main__:app")
