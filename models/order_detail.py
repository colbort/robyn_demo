from tortoise import fields, models


# 订单详情表
class OrderDetail(models.Model):
    id = fields.BigIntField(pk=True)
    order_id = fields.BigIntField()
    product_id = fields.BigIntField()
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    total_price = fields.DecimalField(max_digits=10, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_order_details"
        table_description = "订单详情表"
