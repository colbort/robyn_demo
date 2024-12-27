import json

import pika


class MQRouter:
    def __init__(self):
        self.routes = {}

    def register_handler(self, action):
        """装饰器，用于注册消息处理函数"""

        def decorator(handler):
            self.routes[action] = handler
            return handler  # 返回原函数以支持正常使用

        return decorator

    def handle_message(self, ch, method, properties, message):
        """通用消息分发逻辑"""
        action = message.get("action")
        data = message.get("data")
        handler = self.routes.get(action)
        if not handler:
            response = {"error": f"Unknown action: {action}"}
        else:
            try:
                response = handler(data)
            except Exception as e:
                response = {"error": f"Handler error: {str(e)}"}
        ch.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(response),
        )
