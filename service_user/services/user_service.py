import os
from typing import Tuple, Optional

from tortoise.exceptions import IntegrityError

import service_user.db.user_db as db
from common.logger import logger
from communication.mq_action import *
from handler.router_instance import router
from models.user_account import UserAccount
from service_user.request.req_update import ReqUpdate
from service_user.utils.hash_utils import *


async def register_user(
        email: str,
        phone_country_code: str,
        phone: str,
        password: str,
) -> Tuple[Optional[int], Optional[str], Optional[str]]:
    if not email:
        email = ''
    else:
        if await db.select_user_by_email(email=email):
            raise ValueError(f'邮箱 {email} 已被注册')
    if not phone:
        phone = ''
    else:
        if await db.select_user_by_phone(phone=phone):
            raise ValueError(f'手机号 {phone} 已被注册')
    try:
        salt = os.urandom(16).hex()
        password_hash = hash_password(password, salt)
        user = UserAccount(
            username=generate_unique_username(),
            email=email,
            phone_country_code=phone_country_code,
            phone=phone,
            avatar='',
            password_hash=password_hash,
            salt=salt,
            balance=0.00,
            points=0,
            frozen_amount=0.00,
            status=1,
        )
        return await db.register_user(user)
    except IntegrityError as e:
        # 捕获数据库唯一性约束错误
        logger.error(f"Integrity Error during user registration: {e}")
        return None, None, None
    except Exception as e:
        # 捕获其他错误
        import traceback
        logger.error(f"Unexpected error during user registration: {e}")
        logger.error(traceback.format_exc())
        return None, None, None


async def login_user(
        email: str,
        phone_country_code: str,
        phone: str,
        username: str,
        password: str,
) -> Tuple[Optional[int], Optional[str], Optional[str]]:
    if email:
        user = await db.select_user_by_email(email=email)
    if phone:
        user = await db.select_user_by_phone(phone=phone)
    if username:
        user = await db.select_user_by_username(username=username)
    if not user:
        raise ValueError('用户名或密码错误')
    if not verify_password(password=password, salt=user.salt, hashed_password=user.password_hash):
        raise ValueError('用户名或密码错误')
    return user.id, user.username, user.password_hash


async def logout_user(user_id: str) -> str:
    user = await db.get_user(user_id)
    if not user:
        return "User not found"
    if not user.is_logged_in:
        return "User is not logged in"
    user.is_logged_in = False
    await db.update_user(user)
    return "Logout successful"


@router.register_handler(action_get_user_info)
async def get_user_info(user_id: int) -> Optional[UserAccount]:
    return await db.get_user(user_id)


async def update_user_info(user_id: int, data: ReqUpdate) -> bool:
    user = await db.get_user(user_id)
    if not user:
        raise ValueError("用户不存在")
    if data.email:
        user.email = data.email
    if data.phone_country_code:
        user.phone_country_code = data.phone_country_code
    if data.phone:
        user.phone = data.phone
    if data.password:
        user.password_hash = hash_password(data.password, user.salt)
    if data.avatar:
        user.avatar = data.avatar
    if data.nickname:
        user.nickname = data.nickname
    return await db.update_user(user)


async def __freeze_balance(user_id: int, amount: float):
    """冻结用户余额"""
    user = await db.get_user(user_id)
    if not user:
        return {"error": "User not found"}
    if user.balance < amount:
        return {"error": "Insufficient balance"}
    user.balance -= amount  # 冻结余额
    user.frozen_amount += amount
    if not await db.update_user_balance(user, ["balance", "frozen_amount"]):
        return {"error": "Failed to freeze balance"}
    return {"message": "Balance frozen successfully"}


async def __unfreeze_balance(user_id: int, amount: float):
    """解冻用户余额"""
    user = await db.get_user(user_id)
    if not user:
        return {"error": "User not found"}
    user.balance += amount  # 解冻余额
    user.frozen_amount -= amount
    if not await db.update_user_balance(user, ["balance", "frozen_amount"]):
        return {"error": "Failed to unfreeze balance"}
    return {"message": "Balance unfrozen successfully"}


@router.register_handler(action_freeze_balance)
async def __handle_freeze_balance(data):
    user_id = data["user_id"]
    amount = data["amount"]
    return await __freeze_balance(user_id, amount)


@router.register_handler(action_unfreeze_balance)
async def __handle_unfreeze_balance(data):
    user_id = data["user_id"]
    amount = data["amount"]
    return await __unfreeze_balance(user_id, amount)
