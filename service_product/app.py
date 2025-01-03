import asyncio
import logging

from robyn import Robyn

from communication.mq_consumer import MQConsumer
from config import config as config
from config.settings import *
from handler.db_handler import DBHandler
from handler.redis_handler import RedisHandler
from handler.router_instance import router
from middleware.auth_middleware import AuthenticationMiddleware
from nacos_client.nacos_client import NacosWrapper
from service_product.router.product_router import setup_routes

# 初始化日志记录器
logger = logging.getLogger("robyn")
logger.setLevel(logging.INFO)


# logger = logging.getLogger("pika")
# logger.setLevel(logging.INFO)


def _init_config() -> NacosWrapper:
    nacos = NacosWrapper(
        server_address=SERVER_ADDRESS,
        username=USERNAME,
        password=PASSWORD,
        namespace=NAMESPACE,
    )
    config.config = config.Config(nacos, DATA_ID, GROUP)
    return nacos


def _init_rabbitmq():
    consumer = MQConsumer(
        host=config.Rabbitmq.host(),
        port=config.Rabbitmq.port(),
        username=config.Rabbitmq.username(),
        password=config.Rabbitmq.password(),
        queue_name=config.Product.serviceChannel(),
        router=router,
    )
    from threading import Thread

    Thread(target=consumer.start).start()


async def _init_services():
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
    nacos = _init_config()
    # 服务注册
    nacos.register_service(
        service_name=config.Product.serviceName(),
        port=config.Product.servicePort(),
    )
    # 启动 MQ 消费
    _init_rabbitmq()
    # 初始化数据库、redis
    asyncio.run(_init_services())
    # 启动 HTTP 服务
    app = Robyn(__file__)
    app.configure_authentication(AuthenticationMiddleware())
    setup_routes(app)
    app.start(host="0.0.0.0", port=config.Product.servicePort())
