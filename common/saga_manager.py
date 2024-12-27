class SagaStep:
    """单个事务步骤"""

    def __init__(self, action, compensate):
        self.action = action  # 正常操作
        self.compensate = compensate  # 补偿操作


class SagaManager:
    """SAGA 管理器"""

    def __init__(self):
        self.steps = []
        self.compensations = []

    def add_step(self, action, compensate):
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
            try:
                compensate()
            except Exception as e:
                print(f"Error in compensation: {e}")
