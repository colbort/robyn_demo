from robyn import Robyn

from handler.user_cache_handler import userCache
from service_user.controller.v1 import user_controller as v1


def setup_routes(app: Robyn):
    @app.get("/api/user/health")
    async def health_check(request):
        await userCache.init_cache_handler()
        return {"status": "OK"}

    v1.UserController(app)
