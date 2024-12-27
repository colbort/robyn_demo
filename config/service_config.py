from typing import Optional

from config.config_object import ConfigObject
from nacos_client.nacos_client import NacosWrapper


class ServiceConfig:
    """服务配置管理"""

    def __init__(self, nacos: NacosWrapper, service_name: str):
        self.nacos = nacos
        self.service_name = service_name
        self.config = None

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
        """加载服务配置"""
        service = self.nacos.get_config(f"{self.service_name}.properties", "app-service")
        self.config = ConfigObject(self._parse_config(service))

    def __repr__(self):
        return f"<ServiceConfig {self.service_name}={self.config}>"


config: Optional[ServiceConfig] = None
