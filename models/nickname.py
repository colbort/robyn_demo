from tortoise import fields, models


class Nickname(models.Model):
    """
    昵称表模型
    """
    id = fields.IntField(pk=True, description="ID")
    nickname = fields.CharField(max_length=255, unique=True, description="昵称")
    usage_count = fields.IntField(default=0, description="使用次数")
    deleted = fields.BooleanField(default=False, description="是否删除")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "t_nicknames"  # 映射到数据库表名
        table_description = "昵称表"
