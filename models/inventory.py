from tortoise import fields, models


# 库存表
class Inventory(models.Model):
    id = fields.BigIntField(pk=True)
    product_id = fields.BigIntField()
    quantity = fields.IntField(default=0)
    reserved = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_inventory"
        table_description = "产品表"
