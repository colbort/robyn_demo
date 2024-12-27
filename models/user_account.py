from tortoise import fields, models


# 用户账户表
class UserAccount(models.Model):
    id = fields.BigIntField(pk=True, description="账户ID")
    username = fields.CharField(max_length=50, null=False, unique=True, description="用户名")
    email = fields.CharField(max_length=100, null=True, unique=True, description="电子邮件")
    phone_country_code = fields.CharField(max_length=10, null=False, description="国家编码")
    phone = fields.CharField(max_length=20, null=True, unique=True, description="手机号")
    nickname = fields.CharField(max_length=50, null=False, description="昵称")
    avatar = fields.CharField(max_length=255, null=False, description="头像URL")
    password_hash = fields.CharField(max_length=255, null=False, description="密码哈希值")
    salt = fields.CharField(max_length=32, null=False, description="密码盐")
    balance = fields.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00, description="账户余额")
    points = fields.IntField(default=0, null=False, description="积分")
    frozen_amount = fields.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00,
                                        description="冻结金额")
    status = fields.IntField(default=1, null=False, description="状态 (1:正常, 0:禁用)")
    created_at = fields.DatetimeField(auto_now_add=True, null=False, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, null=False, description="更新时间")

    class Meta:
        table = "t_user_accounts"
        table_description = "用户表"
