class Message:
    def __init__(self, action: str, data: dict):
        """
        初始化消息对象
        :param action: 消息的动作类型
        :param data: 消息携带的数据
        """
        self.action = action
        self.data = data

    def to_dict(self):
        """将消息对象转换为字典格式"""
        return {"action": self.action, "data": self.data}

    def to_json(self):
        """将消息对象转换为 JSON 字符串"""
        import json
        return json.dumps(self.to_dict())
