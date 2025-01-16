import time
from collections import defaultdict
from robyn import Request

from common.logger import logger

TIME_WINDOW = 60  # 时间窗口大小，单位为秒
MAX_REQUESTS_PER_MINUTE = 100  # 每分钟最大请求次数
TOKENS_PER_SECOND = 5  # 每秒钟补充的令牌数量
MAX_TOKENS = 50  # 令牌桶最大令牌数
REDIS_CONNECTION = None  # Redis 连接对象（如果使用 Redis 限流）


class RateLimitMiddleware:
    """限流依赖类，负责检查请求频率"""

    def __init__(self, algorithm: str = "fixed_window"):
        self.algorithm = algorithm
        self.requests = defaultdict(list)
        self.tokens = defaultdict(int)  # 存储每个 IP 的令牌数
        self.last_check_time = defaultdict(float)  # 存储上次检查令牌的时间
        self.redis = REDIS_CONNECTION  # Redis 连接

    async def __call__(self, request: Request):
        """调用该类实例时，检查请求频率"""
        ip = self.__get_client_ip(request)
        logger.info(f"访问地址  {ip}")
        if not ip:
            return None

        if self.algorithm == "fixed_window":
            return await self.__fixed_window(ip)
        elif self.algorithm == "sliding_window":
            return await self.__sliding_window(ip)
        elif self.algorithm == "token_bucket":
            return await self.__token_bucket(ip)
        elif self.algorithm == "leaky_bucket":
            return await self.__leaky_bucket(ip)
        elif self.algorithm == "counter":
            return await self.__counter(ip)
        elif self.algorithm == "redis":
            return await self.__redis(ip)
        elif self.algorithm == "dynamic":
            return await self.__dynamic(ip)
        return None

    async def __fixed_window(self, ip):
        """固定时间窗口限流"""
        current_time = time.time()
        self.requests[ip] = [timestamp for timestamp in self.requests[ip] if current_time - timestamp < TIME_WINDOW]

        if len(self.requests[ip]) >= MAX_REQUESTS_PER_MINUTE:
            return self.__rate_limit_exceeded()

        self.requests[ip].append(current_time)
        return None

    async def __sliding_window(self, ip):
        """滑动时间窗口限流"""
        current_time = time.time()
        self.requests[ip] = [timestamp for timestamp in self.requests[ip] if current_time - timestamp < TIME_WINDOW]

        if len(self.requests[ip]) >= MAX_REQUESTS_PER_MINUTE:
            return self.__rate_limit_exceeded()

        self.requests[ip].append(current_time)
        return None

    async def __token_bucket(self, ip):
        """令牌桶限流"""
        current_time = time.time()

        if ip not in self.last_check_time:
            self.last_check_time[ip] = current_time

        time_diff = current_time - self.last_check_time[ip]
        self.last_check_time[ip] = current_time

        new_tokens = int(time_diff * TOKENS_PER_SECOND)
        self.tokens[ip] = min(self.tokens[ip] + new_tokens, MAX_TOKENS)

        if self.tokens[ip] <= 0:
            return self.__rate_limit_exceeded()

        self.tokens[ip] -= 1
        return None

    async def __leaky_bucket(self, ip):
        """漏桶限流"""
        current_time = time.time()

        if ip not in self.requests:
            self.requests[ip] = []

        # 按漏水速率更新
        self.requests[ip] = [timestamp for timestamp in self.requests[ip] if current_time - timestamp < TIME_WINDOW]

        if len(self.requests[ip]) >= MAX_REQUESTS_PER_MINUTE:
            return self.__rate_limit_exceeded()

        self.requests[ip].append(current_time)
        return None

    async def __counter(self, ip):
        """计数器限流"""
        if ip not in self.requests:
            self.requests[ip] = 0

        self.requests[ip] += 1
        if self.requests[ip] > MAX_REQUESTS_PER_MINUTE:
            return self.__rate_limit_exceeded()

        return None

    async def __redis(self, ip):
        """基于 Redis 的限流"""
        # 如果使用 Redis 连接进行限流，您需要在这里添加 Redis 的实现
        if self.redis:
            current_time = time.time()
            redis_key = f"requests:{ip}"
            current_count = self.redis.get(redis_key) or 0

            if current_count >= MAX_REQUESTS_PER_MINUTE:
                return self.__rate_limit_exceeded()

            self.redis.incr(redis_key)
            self.redis.expire(redis_key, TIME_WINDOW)
            return None
        else:
            return self.__rate_limit_exceeded()

    async def __dynamic(self, ip):
        """动态限流"""
        # 动态限流可以基于服务器的负载来调整请求限流的阈值
        # 例如：如果 CPU 使用率过高，则降低最大请求数
        current_time = time.time()

        # 这里是动态调整的一个简单示例，可以根据系统负载、队列长度等动态调整阈值
        MAX_REQUESTS = self._get_dynamic_limit()

        self.requests[ip] = [timestamp for timestamp in self.requests[ip] if current_time - timestamp < TIME_WINDOW]

        if len(self.requests[ip]) >= MAX_REQUESTS:
            return self.__rate_limit_exceeded()

        self.requests[ip].append(current_time)
        return None

    def __get_dynamic_limit(self):
        """根据当前系统负载调整最大请求数"""
        # 假设有一个获取当前系统负载的函数
        cpu_load = self._get_cpu_load()
        if cpu_load > 80:
            return MAX_REQUESTS_PER_MINUTE // 2  # 负载过高时，限制请求数
        return MAX_REQUESTS_PER_MINUTE

    @classmethod
    def __get_cpu_load(cls):
        """获取 CPU 使用率（模拟）"""
        return 50  # 这里仅为示例，实际中应该使用系统的 API 获取当前 CPU 使用率

    @classmethod
    def __rate_limit_exceeded(cls):
        """限流超标时的响应"""
        return {
            "status": 429,
            "body": "Too many requests, please try again later.",
            "headers": [("Content-Type", "text/plain")]
        }

    @classmethod
    def __get_client_ip(cls, request):
        """获取客户端 IP"""
        addr = request.headers.get('X-Forwarded-For')
        if addr:
            data = addr.split(',')
            if data:
                return data[0]
        return request.ip_addr
