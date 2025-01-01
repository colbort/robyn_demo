import functools
import json
import random
from typing import Any

import aioredis
from aioredis import Redis
from tortoise import models

from common.logger import logger


class RedisHandler:
    _pool: Redis = None

    @staticmethod
    async def init(host: str, port: str, db: str, password: str):
        """
        初始化 Redis 连接池
        """

        # 创建 Redis 连接池
        try:
            RedisHandler._pool = await aioredis.from_url(
                f"redis://{host}:{port}",
                db=db,
                password=password,
                decode_responses=True,  # 自动解码
            )
            logger.info("Redis 初始化完成！")
        except Exception as e:
            logger.error(f"Redis 初始化失败 {e}")

    @staticmethod
    def pool():
        return RedisHandler._pool

    @staticmethod
    async def close():
        """
        关闭 Redis 连接池
        """
        if RedisHandler._pool:
            await RedisHandler._pool.close()
        print("Redis 连接池已关闭")

    @staticmethod
    async def set(key: str, value: str, expire: int = 0):
        """
        设置 Key-Value
        """
        if expire > 0:
            await RedisHandler._pool.set(key, value, ex=expire)
        else:
            await RedisHandler._pool.set(key, value)

    @staticmethod
    async def get(key: str):
        """
        获取 Key 的值
        """
        return await RedisHandler._pool.get(key)

    @staticmethod
    async def delete(key: str):
        """
        删除 Key
        """
        await RedisHandler._pool.delete(key)

    @staticmethod
    async def incr(key: str, amount: int = 1):
        """
        自增 Key 的值
        """
        await RedisHandler._pool.incrby(key, amount)

    @staticmethod
    async def expire(key: str, seconds: int):
        """
        设置 Key 的过期时间
        """
        await RedisHandler._pool.expire(key, seconds)

    @staticmethod
    async def exists(key: str) -> bool:
        """
        判断 Key 是否存在
        """
        return await RedisHandler._pool.exists(key)

    @staticmethod
    async def hset(key: str, field: str, value: str):
        """
        设置哈希表的字段值
        """
        await RedisHandler._pool.hset(key, field, value)

    @staticmethod
    async def hget(key: str, field: str):
        """
        获取哈希表中字段的值
        """
        return await RedisHandler._pool.hget(key, field)

    @staticmethod
    async def hdel(key: str, field: str):
        """
        删除哈希表中的字段
        """
        await RedisHandler._pool.hdel(key, field)

    @staticmethod
    async def hgetall(key: str):
        """
        获取哈希表中的所有字段和值
        """
        return await RedisHandler._pool.hgetall(key)

    @staticmethod
    async def lpush(key: str, *values: str):
        """
        向列表左端添加一个或多个值
        """
        await RedisHandler._pool.lpush(key, *values)

    @staticmethod
    async def rpush(key: str, *values: str):
        """
        向列表右端添加一个或多个值
        """
        await RedisHandler._pool.rpush(key, *values)

    @staticmethod
    async def lpop(key: str):
        """
        从列表左端移除并返回第一个元素
        """
        return await RedisHandler._pool.lpop(key)

    @staticmethod
    async def lrem(key: str, count: int, value: Any):
        """
        从列表左端移除并返回第一个元素
        """
        return await RedisHandler._pool.lrem(key, count, value)

    @staticmethod
    async def rpop(key: str):
        """
        从列表右端移除并返回最后一个元素
        """
        return await RedisHandler._pool.rpop(key)

    @staticmethod
    async def lrange(key: str, start: int, stop: int):
        """
        获取列表指定范围的元素
        """
        return await RedisHandler._pool.lrange(key, start, stop)

    @staticmethod
    async def sadd(key: str, *members: str):
        """
        向集合添加一个或多个成员
        """
        await RedisHandler._pool.sadd(key, *members)

    @staticmethod
    async def smembers(key: str):
        """
        获取集合中的所有成员
        """
        return await RedisHandler._pool.smembers(key)

    @staticmethod
    async def srem(key: str, *members: str):
        """
        从集合中移除一个或多个成员
        """
        await RedisHandler._pool.srem(key, *members)

    @staticmethod
    async def zadd(key: str, *args: tuple):
        """
        向有序集合添加成员及其分数
        """
        await RedisHandler._pool.zadd(key, *args)

    @staticmethod
    async def zrange(key: str, start: int, stop: int):
        """
        获取有序集合中指定范围的成员（按分数排序）
        """
        return await RedisHandler._pool.zrange(key, start, stop)

    @staticmethod
    async def zrem(key: str, *members: str):
        """
        从有序集合中移除一个或多个成员
        """
        await RedisHandler._pool.zrem(key, *members)

    @staticmethod
    async def zscore(key: str, member: str):
        """
        获取有序集合中成员的分数
        """
        return await RedisHandler._pool.zscore(key, member)


def _serialize_object(obj: Any) -> str:
    """
    通用序列化函数，将 ORM 对象序列化为 JSON 字符串。
    :param obj: 要序列化的对象，可以是 ORM 实例或其他数据结构。
    :return: 序列化后的 JSON 字符串
    """
    if isinstance(obj, models.Model):
        # 如果是 Tortoise ORM 模型，可以手动序列化
        return json.dumps(obj.to_dict())
    else:
        raise TypeError("Unsupported object type for serialization")


def _deserialize_object(data: str, cls: Any) -> Any:
    """
    反序列化函数，将 JSON 字符串反序列化为对应的 ORM 对象。
    :param data: 要反序列化的 JSON 字符串
    :param cls: 目标类，ORM 类或其他
    :return: 反序列化后的对象
    """
    if issubclass(cls, models.Model):
        # 如果是 Tortoise ORM 模型，手动从字典构造实例
        dict_data = json.loads(data)  # 将 JSON 字符串转换为字典
        return cls(**dict_data)  # 使用字典构建 ORM 实例
    else:
        raise TypeError("Unsupported object type for deserialization")


def cache_result(redis_type: str = "string", ttl: int = None, key_generator: callable = None, field: str = None,
                 cls: Any = None, key_field: str = 'id', lock_timeout: int = 10):
    """
    Redis 缓存装饰器
    :param redis_type: Redis 数据结构类型，支持 'string', 'hash', 'list', 'set', 'sorted_set'
    :param ttl: 缓存过期时间，单位秒。可以为 None，表示缓存永不过期
    :param key_generator: 用于生成缓存键的函数
    :param field: 如果使用哈希表，则指定缓存字段
    :param cls: 指定返回的 ORM 类或 Pydantic 类
    :param key_field: 用来生成缓存键的字段，如 'phone', 'email', 'id' 等
    :param lock_timeout: 锁的超时时间，单位秒
    """

    def get_cached_result(value_type, cache_key, f):
        """获取缓存结果，根据 Redis 数据类型决定获取方法"""
        if value_type == "string":
            return RedisHandler.get(cache_key)
        elif value_type == "hash":
            return RedisHandler.hget(cache_key, f)
        elif value_type == "list":
            return RedisHandler.lrange(cache_key, 0, -1)
        elif value_type == "set":
            return RedisHandler.smembers(cache_key)
        elif value_type == "sorted_set":
            return RedisHandler.zrange(cache_key, 0, -1)
        return None

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # 根据 key_field 动态生成缓存键
            cache_key = f"{func.__name__}:{kwargs.get(key_field) if key_field in kwargs else args[0]}"

            # 进一步自定义生成缓存键的规则
            if key_generator:
                cache_key = key_generator(key_field, *args, **kwargs)

            if field:
                cache_key = f"{cache_key}:{field}"

            # 尝试获取缓存，如果缓存存在则直接返回
            cached_result = await get_cached_result(redis_type, cache_key, field)
            if cached_result:
                return _deserialize_object(cached_result, cls)

            # 如果缓存未命中，尝试加锁，避免缓存击穿
            lock = RedisHandler.pool().lock(f"lock_{cache_key}", timeout=lock_timeout)  # 锁定缓存键
            async with lock:
                # 双重检查：再次确认缓存是否已经被其他请求更新
                cached_result = await get_cached_result(redis_type, cache_key, field)
                if cached_result:
                    return _deserialize_object(cached_result, cls)

                # 如果没有缓存，调用原函数并将结果缓存
                result = await func(*args, **kwargs)

                # 重新存入更新后的数据
                if ttl is None:
                    # 如果 ttl 为 None，表示缓存永不过期
                    await RedisHandler.set(cache_key, _serialize_object(result))
                else:
                    # 为避免缓存雪崩，给 ttl 添加随机浮动
                    random_ttl = ttl + random.randint(0, 300)  # 随机增加过期时间，防止缓存雪崩
                    if redis_type == "string":
                        await RedisHandler.set(cache_key, _serialize_object(result), expire=random_ttl)
                    elif redis_type == "hash":
                        await RedisHandler.hset(cache_key, field, _serialize_object(result))
                    elif redis_type == "list":
                        await RedisHandler.rpush(cache_key, *map(_serialize_object, result))
                    elif redis_type == "set":
                        await RedisHandler.sadd(cache_key, *map(_serialize_object, result))
                    elif redis_type == "sorted_set":
                        await RedisHandler.zadd(cache_key,
                                                *[(item["score"], _serialize_object(item["value"])) for item in result])

            return result

        return wrapper

    return decorator


async def update_cache(redis_type: str, value: str, result: Any, ttl: int = 3600, field: str = None,
                       cache_key: str = None):
    """
    更新缓存：删除旧的缓存并将更新后的数据存入缓存。
    :param redis_type: Redis 数据结构类型，支持 'string', 'hash', 'list', 'set', 'sorted_set'
    :param key_field: 缓存键字段（如 'id', 'phone', 'email'）
    :param value: 数据的标识值（如 'phone', 'email'）
    :param result: 更新后的数据
    :param ttl: 缓存过期时间（秒）
    :param field: 如果使用哈希表，指定缓存字段
    :param cache_key: 可选，指定缓存键，优先使用此键
    """
    # 如果外部指定了 cache_key，使用指定的 cache_key；否则根据 key_field 和 value 构建 cache_key
    if not cache_key:
        raise ValueError("Missing cache_key")

    # 删除旧缓存
    if redis_type == "string":
        await RedisHandler.delete(cache_key)
    elif redis_type == "hash" and field:
        await RedisHandler.hdel(cache_key, field)
    elif redis_type == "list":
        await RedisHandler.lrem(cache_key, 0, value)  # 删除列表中所有与指定 value 匹配的项
    elif redis_type == "set":
        await RedisHandler.srem(cache_key, value)
    elif redis_type == "sorted_set":
        await RedisHandler.zrem(cache_key, value)

    # 重新存入更新后的数据
    if redis_type == "string":
        await RedisHandler.set(cache_key, _serialize_object(result), expire=ttl)
    elif redis_type == "hash" and field:
        await RedisHandler.hset(cache_key, field, _serialize_object(result))
    elif redis_type == "list":
        await RedisHandler.rpush(cache_key, _serialize_object(result))
    elif redis_type == "set":
        await RedisHandler.sadd(cache_key, _serialize_object(result))
    elif redis_type == "sorted_set":
        await RedisHandler.zadd(cache_key, (result["score"], _serialize_object(result["value"])))


async def delete_cache(redis_type: str, value: str, field: str = None, cache_key: str = None):
    """
    删除缓存：根据指定的键字段和值删除缓存。
    :param redis_type: Redis 数据结构类型，支持 'string', 'hash', 'list', 'set', 'sorted_set'
    :param key_field: 缓存键字段（如 'id', 'phone', 'email'）
    :param value: 数据的标识值（如 'phone', 'email'）
    :param field: 如果使用哈希表，指定缓存字段
    :param cache_key: 可选，指定缓存键，优先使用此键
    """
    # 如果外部指定了 cache_key，使用指定的 cache_key；否则根据 key_field 和 value 构建 cache_key
    if not cache_key:
        raise ValueError("Missing cache_key")

    # 删除缓存
    if redis_type == "string":
        await RedisHandler.delete(cache_key)
    elif redis_type == "hash" and field:
        await RedisHandler.hdel(cache_key, field)
    elif redis_type == "list":
        await RedisHandler.lrem(cache_key, 0, value)  # 删除列表中所有与指定 value 匹配的项
    elif redis_type == "set":
        await RedisHandler.srem(cache_key, value)
    elif redis_type == "sorted_set":
        await RedisHandler.zrem(cache_key, value)
