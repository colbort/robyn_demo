import asyncio
import logging

from robyn import Robyn, DependencyMap

from communication.mq_consumer import MQConsumer
from config import config as config
from config.settings import *
from handler.db_handler import DBHandler
from handler.redis_handler import RedisHandler
from handler.router_instance import router
from handler.translator_handler import Translator
from middleware.auth_middleware import AuthenticationMiddleware
from middleware.i18n_middleware import i18n_handler
from middleware.page_middleware import page_handler
from nacos_client.nacos_client import NacosWrapper
from router.user_router import setup_routes

# 初始化日志记录器
logger = logging.getLogger("robyn")
logger.setLevel(logging.INFO)

# 设置 Tortoise 的 SQL 日志输出
logger = logging.getLogger("tortoise.db_client")
logger.setLevel(logging.INFO)


# logger = logging.getLogger("pika")
# logger.setLevel(logging.INFO)


def __init_config() -> NacosWrapper:
    nanos = NacosWrapper(
        server_address=SERVER_ADDRESS,
        username=USERNAME,
        password=PASSWORD,
        namespace=NAMESPACE,
    )
    config.config = config.Config(nanos, DATA_ID, GROUP)
    return nanos


def __init_rabbitmq():
    consumer = MQConsumer(
        host=config.Rabbitmq.host(),
        port=config.Rabbitmq.port(),
        username=config.Rabbitmq.username(),
        password=config.Rabbitmq.password(),
        queue_name=config.User.serviceChannel(),
        router=router,
    )
    from threading import Thread
    Thread(target=consumer.start).start()


async def __init_services():
    # 初始化 MYSQL
    await DBHandler.init(config.Mysql.write(), config.Mysql.read())
    # 初始化 Redis
    await RedisHandler.init(
        host=config.Redis.host(),
        port=config.Redis.port(),
        db=config.Redis.db(),
        password=config.Redis.password()
    )


if __name__ == "__main__":
    # 注册服务到 Nacos
    ns = __init_config()
    # 服务注册
    ns.register_service(
        service_name=config.User.serviceName(),
        port=config.User.servicePort(),
    )
    __init_rabbitmq()
    # 初始化数据库、redis
    asyncio.run(__init_services())
    # 国际化初始化
    Translator.set_locales(config.Locales.path())
    # 启动 HTTP 服务
    dependencies = DependencyMap()
    dependencies.add_global_dependency(language=i18n_handler)
    dependencies.add_global_dependency(pagination=page_handler)
    app = Robyn(__file__, dependencies=dependencies)
    app.configure_authentication(AuthenticationMiddleware())
    # initCors(app)
    setup_routes(app)
    app.start(host="0.0.0.0", port=config.User.servicePort())
