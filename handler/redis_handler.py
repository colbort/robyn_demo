import aioredis

from common.logger import logger


class RedisHandler:
    _pool = None

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
