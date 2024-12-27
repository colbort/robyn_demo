import logging

# 创建日志器
logger = logging.getLogger(__name__)  # 使用当前模块名作为日志器名称
logger.propagate = False  # 关闭日志传播

# 设置日志器的级别
logger.setLevel(logging.INFO)  # 设置最低日志级别为 DEBUG

# 创建控制台输出处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 设置控制台输出的最低日志级别为 DEBUG

# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
console_handler.setFormatter(formatter)

# 添加处理器到日志器
logger.addHandler(console_handler)
