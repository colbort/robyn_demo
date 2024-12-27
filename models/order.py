from tortoise import fields, models


# 订单表
class Order(models.Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    status = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_orders"
        table_description = "订单表"
