from robyn import Robyn

from service_wallet.controller.v1 import wallet_controller as v1


def setup_routes(app: Robyn):
    @app.get("/api/wallet/health")
    async def health_check(request):
        return {"status": "OK"}

    v1.WalletController(app)
