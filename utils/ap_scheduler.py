from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseSettings, Field

from .log import logger


class Config(BaseSettings):
    apscheduler_config: dict = Field(
        default_factory=lambda: {"apscheduler.timezone": "Asia/Shanghai"})

    class Config:
        extra = "ignore"


plugin_config = Config()
APSscheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


async def start_scheduler():
    if not APSscheduler.running:
        APSscheduler.configure(plugin_config.apscheduler_config)
        APSscheduler.start()
        logger.opt(colors=True).info("<y>定时器模块已开启。</y>")
