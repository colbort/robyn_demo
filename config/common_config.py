from typing import Optional

from config.config_object import ConfigObject
from nacos_client.nacos_client import NacosWrapper


class CommonConfig:
    """公共配置管理"""

    def __init__(self, nacos: NacosWrapper):
        self.nacos = nacos
        self.rabbitmq = None
        self.mysql = None
        self.redis = None

    def _parse_config(self, raw_config):
        """
        解析 Nacos 返回的配置字符串，将其转换为字典。
        :param raw_config: 原始配置字符串
        :return: 配置字典
        """
        config_dict = {}
        for line in raw_config.split(" "):
            # 去掉首尾空格，并忽略空行和无效行
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)  # 按第一个等号分割
            config_dict[key.strip()] = value.strip()
        return config_dict

    def load(self):
        """加载公共配置"""
        # RabbitMQ 配置
        rabbitmq_config = self.nacos.get_config("rabbitmq.properties", "common-config")
        self.rabbitmq = ConfigObject(self._parse_config(rabbitmq_config))

        # MySQL 配置
        mysql_config = self.nacos.get_config("mysql.properties", "common-config")
        self.mysql = ConfigObject(self._parse_config(mysql_config))

        # Redis 配置
        redis_config = self.nacos.get_config("redis.properties", "common-config")
        self.redis = ConfigObject(self._parse_config(redis_config))

    def __repr__(self):
        return f"<CommonConfig RabbitMQ={self.rabbitmq}, MySQL={self.mysql}, Redis={self.redis}>"


config: Optional[CommonConfig] = None
