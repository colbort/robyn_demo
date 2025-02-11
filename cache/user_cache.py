import threading
from typing import Callable, Any

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


class LazyUserCache:
    """延迟初始化的 UserCache"""

    def __init__(self, config_provider: Callable[[], Any]):
        self.config_provider = config_provider
        self._instance = None
        self._lock = threading.Lock()
        self._is_initializing = False  # 标记是否正在初始化

    def __initialize(self):
        """初始化 UserCache 实例"""
        if self._instance is not None:
            return

        with self._lock:
            if self._instance is None and not self._is_initializing:
                self._is_initializing = True  # 标记为正在初始化
                try:
                    config = self.config_provider()
                    if not config:
                        raise RuntimeError("UserCache 配置尚未加载，请先调用 `common_config.load()`")
                    self._instance = UserCache(
                        host=config['host'],
                        port=int(config['port']),
                        password=config['password'],
                        db=int(config['db']),
                    )
                except Exception as e:
                    print(f"初始化失败  {e}")
                finally:
                    self._is_initializing = False  # 初始化完成，清除标记

    def __getattr__(self, name):
        if self._instance is None:
            self.__initialize()
        return getattr(self._instance, name)

