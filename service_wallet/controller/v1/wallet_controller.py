from robyn import Robyn, Request

from common.router_group import RouterGroup
from service_wallet.services.wallet_service import *


class WalletController:
    def __init__(self, app: Robyn):
        self.app = RouterGroup(app, "/api/v1/wallet/")
        self.__setup_routes()

    def __setup_routes(self):
        @self.app.get("withdraws")
        async def __withdraws(request: Request):
            data = request.json()
            user_id = data.get("user_id")
            username = data.get("username")
            password = data.get("password")
            return {
                "message": withdraws(user_id, username, password),
            }

        @self.app.get("recharges")
        async def __recharges(request: Request):
            data = request.json()
            user_id = data.get("user_id")
            username = data.get("username")
            password = data.get("password")
            return {
                "message": recharges(username, password),
            }
