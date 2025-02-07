import threading
import time
from typing import Callable

from common.logger import logger


class SagaStep:
    """单个事务步骤"""
    def __init__(self, action: Callable, compensate: Callable, max_retry=3, retry_delay=2, timeout=5):
        self.action = action  # 正常操作
        self.compensate = compensate  # 补偿操作
        self.max_retry = max_retry  # 最大重试次数
        self.retry_delay = retry_delay  # 重试间隔（秒）
        self.timeout = timeout  # 超时时间（秒）

    def execute_action(self):
        """执行正常操作"""
        self.action()

    def execute_compensate(self):
        """异步执行补偿操作，并设定超时"""
        compensation_thread = threading.Thread(target=self._retry_compensate)
        compensation_thread.start()
        compensation_thread.join(timeout=self.timeout)  # 等待补偿执行，超过超时时间自动结束

    def _retry_compensate(self):
        """补偿操作，并带有重试逻辑"""
        attempts = 0
        last_exception = None  # 记录最后的异常信息

        while attempts < self.max_retry:
            try:
                self.compensate()  # 执行补偿操作
                return
            except Exception as e:
                last_exception = e  # 记录最后的异常信息
                attempts += 1
                if attempts < self.max_retry:
                    time.sleep(self.retry_delay)  # 等待再试

        # 如果补偿仍然失败，记录最后的补偿失败
        if last_exception:
            logger.error(f"Compensation for {self.action.__name__} failed after {self.max_retry} attempts")
            logger.error(f"Final error: {last_exception}")
            # 在此处可以记录更多的上下文信息，例如要补偿的具体内容
            logger.error(f"Details of the compensation action: {self.compensate.__name__}")
            raise last_exception  # 重新抛出最后的异常


class SagaManager:
    """SAGA 管理器"""
    def __init__(self):
        self.steps = []
        self.compensations = []

    def add_step(self, action: Callable, compensate: Callable):
        """添加事务步骤"""
        self.steps.append(SagaStep(action, compensate))

    def execute(self):
        """执行事务"""
        try:
            for step in self.steps:
                step.action()
                self.compensations.append(step.compensate)
        except Exception as e:
            print(f"Error in SAGA execution: {e}")
            self.rollback()
            raise e

    def rollback(self):
        """回滚事务"""
        for compensate in reversed(self.compensations):
            if not compensate:
                continue
            try:
                compensate()
            except Exception as e:
                print(f"Error in compensation: {e}")
