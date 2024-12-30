from robyn import Robyn, Request

from common.cjwt import create_token
from common.router_group import RouterGroup


class WalletController:
    def __init__(self, app: Robyn):
        self.app = RouterGroup(app, "/api/v1/wallet/")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("withdraws")
        async def _withdraws(request: Request):
            data = request.json()
            user_id = data.get("user_id")
            username = data.get("username")
            password = data.get("password")
            return {
                "message": withdraws(user_id, username, password),
                "data": {
                    "token": create_token(user_id)
                }
            }

        @self.app.get("recharges")
        async def _recharges(request: Request):
            data = request.json()
            user_id = data.get("user_id")
            username = data.get("username")
            password = data.get("password")
            return {
                "message": recharges(username, password),
                "data": {
                    "token": create_token(user_id, username)
                }
            }
