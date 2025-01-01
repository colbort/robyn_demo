from communication.mq_action import *
from handler.router_instance import router
from service_product.db.product_db import *


def fetch_all_products():
    """获取商品列表"""
    return get_all_products()


@router.register_handler(action_fetch_product_details)
def fetch_product_details(product_id: str):
    """获取商品详情"""
    product = get_product_by_id(product_id)
    if not product:
        return {"error": "Product not found"}
    return product.dict()


@router.register_handler(action_purchase_product)
def purchase_product(product_id: str, quantity: int):
    """购买商品并更新库存"""
    if quantity <= 0:
        return {"error": "Invalid purchase quantity"}
    success = update_product_stock(product_id, quantity)
    if not success:
        return {"error": "Not enough stock or product not found"}
    return {"message": "Purchase successful"}


def freeze_stock(product_id: str, quantity: int):
    """冻结商品库存"""
    product = get_product(product_id)
    if not product:
        return {"error": "Product not found"}
    if product.stock < quantity:
        return {"error": "Insufficient stock"}
    product.stock -= quantity  # 冻结库存
    if not update_product_stock(product):
        return {"error": "Failed to freeze stock"}
    return {"message": "Stock frozen successfully"}


def unfreeze_stock(product_id: str, quantity: int):
    """解冻商品库存"""
    product = get_product(product_id)
    if not product:
        return {"error": "Product not found"}
    product.stock += quantity  # 解冻库存
    if not update_product_stock(product):
        return {"error": "Failed to unfreeze stock"}
    return {"message": "Stock unfrozen successfully"}


@router.register_handler(action_freeze_stock)
def handle_freeze_stock(data):
    product_id = data["product_id"]
    quantity = data["quantity"]
    return freeze_stock(product_id, quantity)


@router.register_handler(action_unfreeze_stock)
def handle_unfreeze_stock(data):
    product_id = data["product_id"]
    quantity = data["quantity"]
    return unfreeze_stock(product_id, quantity)
