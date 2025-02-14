import traceback

from tortoise import Tortoise, BaseDBAsyncClient
from tortoise.exceptions import IntegrityError, OperationalError

from common.logger import logger
from models import models


class DBHandler:
    _connections = {}  # 缓存连接池

    @staticmethod
    async def init(db_write: dict, db_read: dict):
        """
        初始化数据库连接池，提前加载主库和从库
        """
        try:
            schema = "mysql"  # 这里可以配置 mysql/postgres
            db_config = {
                "connections": {
                    "default": f"{schema}://{db_write['user']}:{db_write['password']}@{db_write['host']}:{db_write['port']}/{db_write['name']}",
                    "read": f"{schema}://{db_read['user']}:{db_read['password']}@{db_read['host']}:{db_read['port']}/{db_read['name']}",
                },
                "apps": {
                    "models": {
                        "models": models,
                        "default_connection": "default"
                    }
                }
            }
            await Tortoise.init(config=db_config)
            DBHandler._connections["default"] = Tortoise.get_connection("default")  # 主库
            DBHandler._connections["read"] = Tortoise.get_connection("read")  # 从库
            logger.info("数据库初始化完成!")
        except Exception as e:
            logger.error(f"数据库初始化失败 {e}")

    @staticmethod
    async def close():
        """
        关闭所有连接
        """
        await Tortoise.close_connections()

    @staticmethod
    def use_write() -> BaseDBAsyncClient:
        """
        切换到主库（写库）连接池
        """
        return DBHandler._connections["default"]

    @staticmethod
    def use_read() -> BaseDBAsyncClient:
        """
        切换到从库（读库）连接池
        """
        return DBHandler._connections["read"]


async def handle_db_operation(func, *args, **kwargs):
    """
    封装数据库操作异常处理
    :param func: 数据库操作的函数
    :param args: 函数参数
    :param kwargs: 函数关键字参数
    :return: 函数执行结果
    """
    try:
        return await func(*args, **kwargs)
    except IntegrityError as e:
        logger.error(f"IntegrityError occurred while executing {func.__name__}: {str(e)}")
        logger.error(f"SQL Error: {e.__cause__}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise e
    except OperationalError as e:
        logger.error(f"OperationalError occurred while executing {func.__name__}: {str(e)}")
        logger.error(f"SQL Error: {e.__cause__}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise e
    except Exception as e:
        logger.error(f"Unknown error occurred while executing {func.__name__}: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise e
