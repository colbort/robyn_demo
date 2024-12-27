import json

import pika

from communication.mq_router import MQRouter


class MQConsumer:
    def __init__(self, host, port, username, password, queue_name, router: MQRouter):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.router = router

    def start(self):
        """启动 MQ 消费者"""
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=30,
            socket_timeout=30,  # 设置超时时间
            blocked_connection_timeout=30
        ))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)

        def on_message(ch, method, properties, body):
            message = json.loads(body)
            self.router.handle_message(ch, method, properties, message)

        channel.basic_consume(queue=self.queue_name, on_message_callback=on_message, auto_ack=True)
        print(f"Listening for messages on queue: {self.queue_name}")
        channel.start_consuming()
