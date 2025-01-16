import traceback


class TransactionException(Exception):
    """分布式事务异常类"""

    def __init__(self, service_name: str, error_message: str, extra_info: dict = None, sql: str = None):
        # 捕获调用栈信息
        exc_type, exc_value, exc_tb = traceback.format_exc().splitlines()[-3:]
        self.service_name = service_name  # 服务名称
        self.error_message = error_message  # 错误信息
        self.file = exc_tb.split(", ")[0]  # 文件路径
        self.line = exc_tb.split(", ")[1].split(":")[1]  # 行号
        self.sql = sql if extra_info else ''  # SQL 语句
        self.extra_info = extra_info or {}

        super().__init__(f"[{self.service_name}] Error: {self.error_message} at {self.file}:{self.line}")

    def __str__(self):
        return f"{self.args[0]} SQL: {self.sql} Extra Info: {self.extra_info}"
