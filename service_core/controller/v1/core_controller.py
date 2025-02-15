from datetime import datetime

from robyn import Robyn, Request

from common.response import success
from common.router_group import RouterGroup
from service_core.services.core_service import *


class CoreController:
    def __init__(self, app: Robyn):
        self.app = RouterGroup(app, "/api/v1/core/")
        self.__setup_routes()

    def __setup_routes(self):
        @self.app.get("settings")
        async def __settings(request: Request):
            data = request.json()
            user_id = data.get("user_id")
            username = data.get("username")
            password = data.get("password")
            return {
                "message": settings(user_id, username, password),
            }

        @self.app.get("version")
        async def __version(request: Request):
            data = request.json()
            user_id = data.get("user_id")
            username = data.get("username")
            password = data.get("password")
            return {
                "message": version(username, password),
            }

        @self.app.get('time_sync')
        async def __time_sync():
            """
            时间戳同步
            返回服务端 UTC 时间戳（毫秒）。
            公式：
                RTT = (响应时间 - 请求时间)
                时间偏移 = 服务端时间 - (请求时间 + RTT / 2)
                同步后客户端时间 = 当前客户端时间 + 时间偏移
            """
            server_time = int(datetime.utcnow().timestamp() * 1000)  # 毫秒级时间戳
            return success(data=server_time)
