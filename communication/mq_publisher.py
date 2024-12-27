import json
import threading
import time
import uuid
from typing import Callable, Any, Optional

import pika

from communication.mq_message import Message


class MQPublisher:
    def __init__(self, host, port, username, password):
        self.callback_queue = None
        self.response_queue = None
        self.channel = None
        self.connection = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        """建立 RabbitMQ 连接"""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=30,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.response_queue = self.channel.queue_declare(queue="", exclusive=True).method.queue
        self.callback_queue = {}
        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self._on_response,
            auto_ack=True
        )
        # 启动一个线程或后台任务定期调用 process_data_events
        threading.Thread(target=self._keep_alive, daemon=True).start()

    def _keep_alive(self):
        """保持心跳"""
        while not self.connection.is_closed:
            self.connection.process_data_events(time_limit=1)
            time.sleep(10)

    def reconnect(self):
        """重连机制"""
        while True:
            try:
                self.connect()
                break
            except Exception as e:
                print(f"Reconnection failed: {e}")
                time.sleep(2)  # 重连前等待

    def _on_response(self, ch, method, properties, body):
        """处理 RPC 响应"""
        correlation_id = properties.correlation_id
        if correlation_id in self.callback_queue:
            self.callback_queue[correlation_id] = json.loads(body)

    def publish(self, queue_name, message: Message, rpc=False, timeout=5):
        """发布消息"""
        try:
            if self.connection.is_closed:
                self.reconnect()  # 重新连接
            return self._publish_internal(queue_name, message, rpc, timeout)
        except Exception as e:
            print(f"message publish failed {e}")
            self.reconnect()
            return self._publish_internal(queue_name, message, rpc, timeout)

    def _publish_internal(self, queue_name, message: Message, rpc, timeout):
        if rpc:
            correlation_id = str(uuid.uuid4())
            self.callback_queue[correlation_id] = None

            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                properties=pika.BasicProperties(
                    reply_to=self.response_queue,
                    correlation_id=correlation_id
                ),
                body=message.to_json()
            )

            start_time = time.time()
            while self.callback_queue[correlation_id] is None:
                self.connection.process_data_events(time_limit=1)
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    raise TimeoutError("RPC call timed out")
            return self.callback_queue.pop(correlation_id)
        else:
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message.to_json()
            )
            return None

    def close(self):
        if not self.connection.is_closed:
            self.connect()
            self.connection.close()


publisher: Optional[MQPublisher] = None


class LazyMQPublisher:
    """延迟初始化的 MQPublisher"""

    def __init__(self, config_provider: Callable[[], Any]):
        self.config_provider = config_provider
        self._instance = None
        self._lock = threading.Lock()
        self._is_initializing = False  # 标记是否正在初始化

    def _initialize(self):
        """初始化 MQPublisher 实例"""
        if self._instance is not None:
            return

        with self._lock:
            if self._instance is None and not self._is_initializing:
                self._is_initializing = True  # 标记为正在初始化
                try:
                    config = self.config_provider()
                    if not config:
                        raise RuntimeError("RabbitMQ 配置尚未加载，请先调用 `common_config.load()`")
                    self._instance = MQPublisher(
                        host=config['host'],
                        port=int(config['port']),
                        username=config['username'],
                        password=config['password'],
                    )
                except Exception as e:
                    print(f"初始化失败  {e}")
                finally:
                    self._is_initializing = False  # 初始化完成，清除标记

    def __getattr__(self, name):
        if self._instance is None:
            self._initialize()
        return getattr(self._instance, name)
