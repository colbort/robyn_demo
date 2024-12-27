from tortoise import fields, models


# 用户充值表
class UserRecharge(models.Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_method = fields.CharField(max_length=50)
    original_currency = fields.CharField(max_length=10)
    exchange_rate = fields.DecimalField(max_digits=10, decimal_places=6)
    status = fields.IntField(default=0)
    reviewer = fields.CharField(max_length=50, default="")
    remark = fields.CharField(max_length=255, default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_user_withdrawals"
        table_description = "用户充值表"
