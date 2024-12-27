import socket
import threading

import requests
import yaml
from nacos_py import NacosClient


class NacosWrapper:
    def __init__(self, server_address: str, username: str, password: str, namespace: str):
        self.client = NacosClient(server_address, username=username, password=password, namespace=namespace)

    def __get_public_ip(self):
        services = [
            "https://ipinfo.io/ip",
            "http://whatismyip.akamai.com",
            "https://api64.ipify.org",
            "https://checkip.amazonaws.com",
        ]
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except requests.RequestException as e:
                print(f"Failed to fetch public IP from {service}: {e}")
        raise RuntimeError("Unable to fetch public IP from all sources")

    def __get_local_ip(self):
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    def __get_service_ip(self):
        try:
            return self.__get_public_ip()
        except RuntimeError:
            return self.__get_local_ip()

    def get_config(self, data_id: str, group: str):
        config = self.client.get_config(data_id, group)
        if not config:
            raise ValueError(f"配置未找到，请检查 Nacos 中是否已设置对应的 {data_id} 和 {group}")
        return yaml.safe_load(config)

    def send_heartbeat(self, service_name, ip, port, interval=5):
        def heartbeat():
            while True:
                try:
                    self.client.send_heartbeat(service_name, ip, port)
                except Exception as e:
                    print(f"Failed to send heartbeat: {e}")
                threading.Event().wait(interval)  # 每隔 interval 秒发送一次心跳

        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()

    def register_service(self, service_name, port):
        ip = self.__get_service_ip()
        print(f"Service {service_name} registered on {ip}:{port}")
        if self.client.add_naming_instance(service_name, ip, port):
            self.send_heartbeat(service_name, ip, port)
        else:
            print(f"服务 {service_name} 注册失败；{ip}:{port}")

    def discover_service(self, service_name):
        instances = self.client.get_naming_instance(service_name)
        if not instances:
            raise RuntimeError(f"No instances found for service: {service_name}")
        return instances[0]["ip"], instances[0]["port"]
