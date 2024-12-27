from typing import Optional

from nacos_client.nacos_client import NacosWrapper


class Config:
    def __init__(self, nacos: NacosWrapper, data_id: str, group: str):
        """
        初始化 Config 类并加载 YAML 配置文件内容。

        :param nacos: YAML 配置文件内容
        """
        self._config_data = nacos.get_config(data_id, group)

    def get(self, *keys, default=None):
        """
        通过键路径获取配置项的值。

        :param keys: 键路径 (例如: "mysql", "host")
        :param default: 如果键不存在，返回默认值
        :return: 配置值或默认值
        """
        data = self._config_data
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return default
        return data

    def __getattr__(self, item):
        """
        支持通过属性访问顶级配置块 (例如: config.mysql['port'])。

        :param item: 顶级配置块名称
        :return: 对应的配置字典
        """
        try:
            print("11111111111")
            if item in self._config_data:
                return self._config_data[item]
            raise AttributeError(f"No such configuration section: {item}")
        except Exception as e:
            print(f"获取配置 {item} 错误 {e}")
            return ""

    def __repr__(self):
        return f"Config({self._config_data})"


config: Optional[Config] = None


class User:
    @staticmethod
    def serviceName() -> str:
        return config.get("service_user", "name")

    @staticmethod
    def servicePort() -> str:
        return config.get("service_user", "port")

    @staticmethod
    def serviceChannel() -> str:
        return config.get("service_user", "channel")


class Order:
    @staticmethod
    def serviceName() -> str:
        return config.get("service_order", "name")

    @staticmethod
    def servicePort() -> str:
        return config.get("service_order", "port")

    @staticmethod
    def serviceChannel() -> str:
        return config.get("service_order", "channel")


class Product:
    @staticmethod
    def serviceName() -> str:
        return config.get("service_product", "name")

    @staticmethod
    def servicePort() -> str:
        return config.get("service_product", "port")

    @staticmethod
    def serviceChannel() -> str:
        return config.get("service_product", "channel")


class Wallet:
    @staticmethod
    def serviceName() -> str:
        return config.get("service_wallet", "name")

    @staticmethod
    def servicePort() -> str:
        return config.get("service_wallet", "port")

    @staticmethod
    def serviceChannel() -> str:
        return config.get("service_wallet", "channel")


class Core:
    @staticmethod
    def serviceName() -> str:
        return config.get("service_core", "name")

    @staticmethod
    def servicePort() -> str:
        return config.get("service_core", "port")

    @staticmethod
    def serviceChannel() -> str:
        return config.get("service_core", "channel")


class Rabbitmq:
    @staticmethod
    def host() -> str:
        return config.get("rabbitmq", "host")

    @staticmethod
    def port() -> str:
        return config.get("rabbitmq", "port")

    @staticmethod
    def username() -> str:
        return config.get("rabbitmq", "username")

    @staticmethod
    def password() -> str:
        return config.get("rabbitmq", "password")


class Redis:
    @staticmethod
    def host() -> str:
        return config.get("redis", "host")

    @staticmethod
    def port() -> str:
        return config.get("redis", "port")

    @staticmethod
    def db() -> str:
        return config.get("redis", "db")

    @staticmethod
    def password() -> str:
        return config.get("redis", "password")


class Mysql:
    @staticmethod
    def write() -> str:
        return config.get("mysql", "write")

    @staticmethod
    def read() -> str:
        return config.get("mysql", "read")


class Locales:
    @staticmethod
    def path() -> str:
        return config.get("locales", "path")
