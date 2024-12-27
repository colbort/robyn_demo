from tortoise import Tortoise, BaseDBAsyncClient

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
            db_config = {
                "connections": {
                    "default": {
                        "engine": "tortoise.backends.mysql",
                        "credentials": {
                            "host": db_write['host'],
                            "port": db_write['port'],
                            "user": db_write['user'],
                            "password": db_write['password'],
                            "database": db_write['name'],
                        }
                    },
                    "read": {
                        "engine": "tortoise.backends.mysql",
                        "credentials": {
                            "host": db_read['host'],
                            "port": db_read['port'],
                            "user": db_read['user'],
                            "password": db_read['password'],
                            "database": db_read['name'],
                        }
                    }
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
    async def use_write() -> BaseDBAsyncClient:
        """
        切换到主库（写库）连接池
        """
        return DBHandler._connections["default"]

    @staticmethod
    async def use_read() -> BaseDBAsyncClient:
        """
        切换到从库（读库）连接池
        """
        return DBHandler._connections["read"]
