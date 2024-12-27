from typing import List, Optional

from models.order import Order

# 模拟订单数据库
ORDERS_DB = {}


def get_orders_by_user_id(user_id: str) -> List[Order]:
    """根据用户 ID 获取订单列表"""
    return [order for order in ORDERS_DB.values() if order.user_id == user_id]


def get_order_by_id(order_id: str) -> Optional[Order]:
    """根据订单 ID 获取订单详情"""
    return ORDERS_DB.get(order_id)


def create_order(order: Order) -> bool:
    """创建订单"""
    if order.order_id in ORDERS_DB:
        return False
    ORDERS_DB[order.order_id] = order
    return True


def update_order_status(order_id: str, status: str) -> bool:
    """更新订单状态"""
    order = ORDERS_DB.get(order_id)
    if not order:
        return False
    order.status = status
    return True
