import os

# 根据环境变量获取当前环境
env = os.getenv("ENV", "prod")

# 配置不同环境的 Nacos 服务地址和命名空间
CONFIG = {
    "dev": {
        "SERVER_ADDRESS": "http://127.0.0.1:8848",
        "NAMESPACE": "16c3a2e3-a9c2-43d2-b4eb-d51ac0e167a4",
        "USERNAME": "nacos",
        "PASSWORD": "123456"
    },
    "prod": {
        "SERVER_ADDRESS": "http://mall-nacos:8848",
        "NAMESPACE": "087dbe1b-e6f2-488b-97b4-1fbe5f510086",
        "USERNAME": "nacos",
        "PASSWORD": "123456"
    }
}

# Nacos 服务配置信息
SERVER_ADDRESS = CONFIG[env]["SERVER_ADDRESS"]
NAMESPACE = CONFIG[env]["NAMESPACE"]
USERNAME = CONFIG[env]["USERNAME"]  # 用户名
PASSWORD = CONFIG[env]["PASSWORD"]  # 密码
DATA_ID = "mall.yaml"  # 数据 ID
GROUP = "DEFAULT_GROUP"  # 分组名称
