from robyn import Robyn, Request

from common.identify_parse import get_user_id
from common.router_group import RouterGroup
from service_order.services.order_service import *


class OrderController:
    def __init__(self, app: Robyn):
        self.app = RouterGroup(app, "/api/v1/order/")
        self.__setup_routers()

    def __setup_routers(self):
        @self.app.get("orders", auth_required=True)
        async def __get_user_orders(request):
            """获取用户订单列表"""
            user_id = request.query.get("user_id")
            if not user_id:
                return {"error": "User ID is required"}
            return {"orders": fetch_user_orders(user_id)}

        @self.app.get("orders/{order_id}", auth_required=True)
        async def __get_order_details(request, order_id):
            """获取订单详情"""
            return fetch_order_details(order_id)

        @self.app.post("order", auth_required=True)
        async def __create_order(request: Request):
            """创建订单"""
            user_id = get_user_id(request.identity)
            data = request.json()
            items = data.get("items")
            if not user_id or not items:
                return {"error": "User ID and items are required"}
            return create_new_order(user_id, items)

        @self.app.post("orders/{order_id}/confirm", auth_required=True)
        async def __confirm_delivery(request, order_id):
            """确认收货"""
            return confirm_order_delivery(order_id)
