import time
from collections import defaultdict
from robyn import Request

from common.logger import logger

MAX_REQUESTS_PER_MINUTE = 30  # 每分钟最多请求 60 次
TIME_WINDOW = 60  # 限流的时间窗口，单位为秒


def _get_client_ip(request: Request):
    logger.info(f"请求头 {request.headers}")
    addr = request.headers.get('X-Forwarded-For')
    if addr:
        data = addr.split(',')
        if data:
            return data[0]
    return request.ip_addr


class RateLimitMiddleware:
    """限流依赖类，负责检查请求频率"""

    def __init__(self):
        self.requests = defaultdict(list)

    async def __call__(self, request: Request):
        """调用该类实例时，检查请求频率"""
        ip = _get_client_ip(request)
        logger.info(f"访问地址  {ip}")
        if ip:
            # 获取当前时间戳
            current_time = time.time()
            # 清除过期的请求记录
            self.requests[ip] = [timestamp for timestamp in self.requests[ip] if current_time - timestamp < TIME_WINDOW]

            # 判断当前请求是否超出限制
            if len(self.requests[ip]) >= MAX_REQUESTS_PER_MINUTE:
                # 超过请求限制，返回 429 错误
                return {
                    "status": 429,
                    "body": "Too many requests, please try again later.",
                    "headers": [("Content-Type", "text/plain")]
                }

            # 否则，允许请求继续并记录当前时间
            self.requests[ip].append(current_time)
        return None


