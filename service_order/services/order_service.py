import uuid

from common.saga_manager import SagaManager
from communication import mq_publisher as publisher
from communication.mq_action import *
from communication.mq_message import Message
from config import config as config
from service_order.db.order_db import *


def fetch_user_orders(user_id: str):
    """获取用户订单列表"""
    return [order.dict() for order in get_orders_by_user_id(user_id)]


def fetch_order_details(order_id: str):
    """获取订单详情"""
    order = get_order_by_id(order_id)
    if not order:
        return {"error": "Order not found"}
    return order.dict()


def create_new_order(user_id, items):
    """创建订单并保证分布式事务一致性"""
    saga = SagaManager()
    order_id = str(uuid.uuid4())
    total_price = sum(item["quantity"] * item["price"] for item in items)

    def __lock_user_balance():
        """冻结用户余额"""
        data = {"user_id": user_id, "amount": total_price}
        message = Message(action=action_freeze_balance, data=data)
        response = publisher.publisher.publish(config.User.serviceChannel(), message, rpc=True)
        if "error" in response:
            raise Exception(response["error"])

    def __unlock_user_balance():
        """解冻用户余额"""
        data = {"user_id": user_id, "amount": total_price}
        message = Message(action=action_unfreeze_balance, data=data)
        publisher.publisher.publish(config.User.serviceChannel(), message, rpc=True)

    def __lock_product_stock():
        """锁定商品库存"""
        data = []
        for item in items:
            data = data.append({"product_id": item["product_id"], "quantity": item["quantity"]})
        message = Message(action=action_freeze_stock, data=data)
        response = publisher.publisher.publish(config.Product.serviceChannel(), message, rpc=True)
        if "error" in response:
            raise Exception(response["error"])

    def __unlock_product_stock():
        """解锁商品库存"""
        data = []
        for item in items:
            data = data.append({"product_id": item["product_id"], "quantity": item["quantity"]})
        message = Message(action=action_unfreeze_stock, data=data)
        publisher.publisher.publish(config.Product.serviceChannel(), message, rpc=True)

    def __create_order_record():
        """生成订单记录"""
        order = Order(
            user_id=user_id, total_price=total_price, status=0
        )
        if not create_order(order):
            raise Exception("Failed to create order record")

    # 添加事务步骤
    saga.add_step(__lock_user_balance, __unlock_user_balance)
    saga.add_step(__lock_product_stock, __unlock_product_stock)
    saga.add_step(__create_order_record, lambda: None)  # 创建订单无需补偿

    # 执行事务
    try:
        saga.execute()
        return {"message": "Order created successfully", "order_id": order_id}
    except Exception as e:
        # 返回详细的错误信息给调用方
        print(f"[Error] Transaction failed for order {order_id}: {e}")
        return {"message": "Transaction failed", "error": str(e), "order_id": order_id}


def confirm_order_delivery(order_id: str):
    """确认订单收货"""
    success = update_order_status(order_id, "Delivered")
    if not success:
        return {"error": "Order not found or cannot be updated"}
    return {"message": "Order confirmed as delivered"}
