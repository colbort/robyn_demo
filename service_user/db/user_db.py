from typing import Optional, Tuple

from tortoise.transactions import in_transaction

from common.logger import logger
from handler.db_handler import DBHandler
from models.nickname import Nickname
from models.user_account import UserAccount


# from tortoise.expressions import Q


async def register_user(user: UserAccount) -> Tuple[Optional[int], Optional[str]]:
    async with in_transaction("default") as conn:
        # 获取昵称
        nickname = await Nickname.filter(deleted=False).order_by("usage_count", "id").using_db(conn).first()
        if not nickname:
            logger.error("No available nickname found!")
            return None, None

        # 更新昵称使用计数
        nickname.usage_count += 1
        await nickname.save(using_db=conn)
        user.nickname = nickname.nickname
        await user.save(using_db=conn)
        return user.id, user.username


async def select_user_by_email(email: str) -> Optional[UserAccount]:
    try:
        await DBHandler.use_read()
        return await UserAccount.filter(email=email).first()
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


async def select_user_by_phone(phone: str) -> Optional[UserAccount]:
    try:
        await DBHandler.use_read()
        return await UserAccount.filter(phone=phone).first()
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


async def select_user_by_username(username: str) -> Optional[UserAccount]:
    try:
        await DBHandler.use_read()
        return await UserAccount.filter(username=username).first()
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


async def get_user(user_id: int) -> Optional[UserAccount]:
    try:
        await DBHandler.use_read()
        user = await UserAccount.filter(id=user_id).first()
        return user
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


async def update_user(user: UserAccount) -> bool:
    try:
        await DBHandler.use_write()
        await user.save()
        return True
    except Exception as e:
        logger.error(f'更新用户信息失败 {e}')
        return False


async def update_user_balance(user: UserAccount) -> bool:
    try:
        await DBHandler.use_write()
        await user.save()
        return True
    except Exception as e:
        logger.error(f'更新用户余额失败 {e}')
        return False
