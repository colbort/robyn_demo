from robyn import Robyn

from service_product.controller.v1 import product_controller as v1


def setup_routes(app: Robyn):
    @app.get("/api/product/health")
    async def health_check(request):
        return {"status": "OK"}

    v1.ProductController(app)
