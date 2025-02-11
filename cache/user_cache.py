from common.logger import logger
from cache.memery_cache_base import MemoryCacheHandler
from service_user.db.user_db import select_all


class UserCache(MemoryCacheHandler):
    def __init__(self, host='localhost', port=6379, password="", db=0, channel='user_update_channel'):
        super().__init__(host, port, password, db, channel)

    async def init_cache_handler(self):
        logger.info("开始初始化用户缓存")
        users = await select_all()
        for user in users:
            self.memory_cache[user.username] = user.password_hash
        logger.info("用户缓存初始化完成")


