from tortoise import fields, models


# 用户交易记录表
class UserTransaction(models.Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    transaction_type = fields.IntField()
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    balance_before = fields.DecimalField(max_digits=10, decimal_places=2)
    balance_after = fields.DecimalField(max_digits=10, decimal_places=2)
    remark = fields.CharField(max_length=255, default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "t_user_recharges"
        table_description = "用户交易记录表"
