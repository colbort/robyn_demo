from typing import Optional

from models.user_account import User

# 模拟用户数据库
USER_DB = {}


def create_user(user: User) -> bool:
    if user.user_id in USER_DB:
        return False
    USER_DB[user.user_id] = user
    return True


def get_user(user_id: str) -> Optional[User]:
    return USER_DB.get(user_id)


def update_user(user: User) -> bool:
    if user.user_id not in USER_DB:
        return False
    USER_DB[user.user_id] = user
    return True


def update_user_balance(user: User) -> bool:
    """
    更新用户余额。
    如果用户不存在，返回 False；如果更新成功，返回 True。
    """
    if user.user_id not in USER_DB:
        return False
    USER_DB[user.user_id] = user
    return True
