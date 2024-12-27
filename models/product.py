from tortoise import fields, models


# 产品表
class Product(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField(default=0)
    status = fields.IntField(default=1)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_products"
        table_description = "产品表"
