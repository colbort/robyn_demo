from communication.mq_publisher import LazyMQPublisher
from config import config as config


def _provide_config():
    return config.config.rabbitmq


publisher = LazyMQPublisher(_provide_config)
