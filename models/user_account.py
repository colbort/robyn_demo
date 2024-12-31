from datetime import datetime
from decimal import Decimal

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

    def to_dict(self):
        """
        手动序列化为字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone_country_code": self.phone_country_code,
            "phone": self.phone,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "balance": str(self.balance) if isinstance(self.balance, Decimal) else self.balance,
            "points": self.points,
            "frozen_amount": str(self.frozen_amount) if isinstance(self.frozen_amount, Decimal) else self.frozen_amount,
            "status": self.status,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
