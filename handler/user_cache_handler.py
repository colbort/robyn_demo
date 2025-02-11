from cache.lazy_init import LazyCache
from cache.user_cache import UserCache
from config import config as config


def _provide_config():
    return config.config.redis


userCache = LazyCache(UserCache, _provide_config)
