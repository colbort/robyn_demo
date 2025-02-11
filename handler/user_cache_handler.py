from cache.user_cache import LazyUserCache
from config import config as config


def _provide_config():
    return config.config.redis


userCache = LazyUserCache(_provide_config)
