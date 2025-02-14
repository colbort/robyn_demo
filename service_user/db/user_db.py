from typing import Optional, Tuple, List

from tortoise.transactions import in_transaction

from common.logger import logger
from handler.db_handler import DBHandler, handle_db_operation
from handler.redis_handler import cache_result, delete_cache
from models.nickname import Nickname
from models.user_account import UserAccount


# from tortoise.expressions import Q

def generate_user_cache_key(key_field, *args, **kwargs) -> str:
    field = kwargs.get(key_field)
    if field:
        return f"user:{field}"
    return f"user:{args[0]}"


async def register_user(user: UserAccount) -> Tuple[Optional[int], Optional[str]]:
    async with in_transaction("default") as conn:
        # 获取昵称
        nickname = await Nickname.filter(deleted=False).order_by("usage_count", "id").using_db(conn).first()
        if not nickname:
            logger.error("No available nickname found!")
            return None, None, None

        # 更新昵称使用计数
        nickname.usage_count += 1
        await nickname.save(using_db=conn)
        user.nickname = nickname.nickname
        await user.save(using_db=conn)
        return user.id, user.username, user.password_hash


@cache_result(redis_type="string", key_generator=generate_user_cache_key, key_field="email", cls=UserAccount)
async def select_user_by_email(email: str) -> Optional[UserAccount]:
    try:
        DBHandler.use_read()
        return await UserAccount.filter(email=email).first()
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


@cache_result(redis_type="string", key_generator=generate_user_cache_key, key_field="phone", cls=UserAccount)
async def select_user_by_phone(phone: str) -> Optional[UserAccount]:
    try:
        DBHandler.use_read()
        return await UserAccount.filter(phone=phone).first()
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


@cache_result(redis_type="string", key_generator=generate_user_cache_key, key_field="username", cls=UserAccount)
async def select_user_by_username(username: str) -> Optional[UserAccount]:
    try:
        DBHandler.use_read()
        return await UserAccount.filter(username=username).first()
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


@cache_result(redis_type="string", key_generator=generate_user_cache_key, cls=UserAccount)
async def get_user(user_id: int) -> Optional[UserAccount]:
    try:
        DBHandler.use_read()
        user = await UserAccount.filter(id=user_id).first()
        return user
    except Exception as e:
        logger.error(f'查询失败 {e}')
        return None


async def update_user(user: UserAccount) -> bool:
    try:
        DBHandler.use_write()
        await user.save()
        return True
    except Exception as e:
        logger.error(f'更新用户信息失败 {e}')
        return False


async def update_user_balance(user: UserAccount) -> bool:
    try:
        DBHandler.use_write()
        await handle_db_operation(user.save)
        await delete_cache(redis_type="string", cache_key=f"user:{user.id}")
        await delete_cache(redis_type="string", cache_key=f"user:{user.phone}")
        await delete_cache(redis_type="string", cache_key=f"user:{user.email}")
        await delete_cache(redis_type="string", cache_key=f"user:{user.username}")
        return True
    except Exception as e:
        logger.error(f'更新用户余额失败 {e}')
        raise e


async def select_all() -> List[UserAccount]:
    try:
        DBHandler.use_read()
        users = await UserAccount.all()
        return users
    except Exception as e:
        raise e
