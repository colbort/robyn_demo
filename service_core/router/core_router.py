from robyn import Robyn

from service_core.controller.v1 import core_controller as v1


def setup_routes(app: Robyn):
    @app.get("/api/core/health")
    async def health_check(request):
        return {"status": "OK"}

    v1.CoreController(app)
