import threading
from typing import Callable, Any


class LazyCache:
    """延迟初始化的 LazyCache"""

    def __init__(self, cache_class: Callable[[], Any], config_provider: Callable[[], Any]):
        self.cache_class = cache_class
        self.config_provider = config_provider
        self._instance = None
        self._lock = threading.Lock()
        self._is_initializing = False  # 标记是否正在初始化

    def __initialize(self):
        """初始化 LazyCache 实例"""
        if self._instance is not None:
            return

        with self._lock:
            if self._instance is None and not self._is_initializing:
                self._is_initializing = True  # 标记为正在初始化
                try:
                    config = self.config_provider()
                    if not config:
                        raise RuntimeError("LazyCache 配置尚未加载，请先调用 `common_config.load()`")
                    self._instance = self.cache_class(
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