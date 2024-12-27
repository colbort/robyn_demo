from robyn import Robyn

from service_order.controller.v1 import order_controller as v1


def setup_routes(app: Robyn):
    @app.get("/api/order/health")
    async def health_check(request):
        return {"status": "OK"}

    v1.OrderController(app)
