from robyn import Robyn, Request

from common.router_group import RouterGroup
from service_product.services.product_service import *


class ProductController:
    def __init__(self, app: Robyn):
        self.app = RouterGroup(app, "/api/v1/product/")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("products")
        async def _get_products(request):
            """获取商品列表"""
            return {"products": [product.dict() for product in fetch_all_products()]}

        @self.app.get("products/{product_id}")
        async def _get_product_details(request, product_id):
            """获取商品详情"""
            return fetch_product_details(product_id)

        @self.app.post("products/purchase")
        async def _purchase_product_controller(request: Request):
            """购买商品"""
            data = request.json()
            product_id = data.get("product_id")
            quantity = data.get("quantity")
            return purchase_product(product_id, quantity)
