from typing import List, Optional

from models.product import Product

# 模拟商品数据库
PRODUCTS_DB = {
    "1": Product(product_id="1", name="Product A", price=10.0, stock=100),
    "2": Product(product_id="2", name="Product B", price=20.0, stock=50),
    "3": Product(product_id="3", name="Product C", price=30.0, stock=30),
}


def get_all_products() -> List[Product]:
    """获取所有商品"""
    return list(PRODUCTS_DB.values())


def get_product_by_id(product_id: str) -> Optional[Product]:
    """根据商品 ID 获取商品"""
    return PRODUCTS_DB.get(product_id)


def get_product(product_id: str) -> Optional[Product]:
    """根据商品 ID 获取商品信息"""
    return PRODUCTS_DB.get(product_id)


def update_product_stock(product: Product) -> bool:
    """
    更新商品库存。
    如果商品不存在，返回 False；如果更新成功，返回 True。
    """
    if product.product_id not in PRODUCTS_DB:
        return False
    PRODUCTS_DB[product.product_id] = product
    return True
