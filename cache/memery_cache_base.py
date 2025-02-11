import json
from abc import ABC, abstractmethod
from threading import Thread
import redis
from common.logger import logger


class MemoryCacheHandler(ABC):
    def __init__(self, host='localhost', port=6379, password="", db=0, channel='data_update_channel'):
        try:
            # 使用同步 Redis 客户端
            self._pool = redis.StrictRedis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True  # 自动解码
            )
            logger.info("Redis 初始化完成！")
        except Exception as e:
            logger.error(f"Redis 发布/订阅初始化失败 {e}")

        # 内存缓存数据存储
        self.memory_cache = {}
        # Redis Pub/Sub 频道
        self.channel = channel

        # 启动子线程来执行订阅
        self._start_subscribe_mq()

    def publish_mq(self, key: str, data: str):
        """发布消息到 Redis MQ (Pub/Sub)"""
        message = {
            "action": "update",
            "key": key,
            "data": data
        }
        # 使用同步的发布操作
        self._pool.publish(self.channel, json.dumps(message))

    def _start_subscribe_mq(self):
        """在子线程中开始订阅 Redis 消息更新"""
        # 启动一个新线程来执行订阅逻辑
        thread = Thread(target=self._subscribe_mq)
        thread.daemon = True
        thread.start()

    def _subscribe_mq(self):
        """订阅 Redis 频道并更新缓存"""
        pubsub = self._pool.pubsub()
        pubsub.subscribe(self.channel)

        # 持续监听消息队列（同步方式）
        for message in pubsub.listen():
            if message["type"] == "message":
                self._update_cache_from_message(message)

    def _update_cache_from_message(self, message):
        """处理更新缓存的逻辑"""
        data = json.loads(message["data"])
        self.memory_cache[data['key']] = data["data"]  # 更新本地缓存
        logger.info(f"Cache updated via MQ: {data}")

    def get_cache_value(self, key: str) -> str:
        """从内存缓存中获取数据"""
        return self.memory_cache.get(key)

    @abstractmethod
    def init_cache_handler(self):
        """抽象方法：具体的服务需要实现这个方法来初始化自己的缓存数据"""
        pass
