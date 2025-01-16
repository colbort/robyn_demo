# 使用 Python 3.10 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 更新系统并安装构建工具
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libssl-dev \
    libffi-dev \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 将项目代码复制到容器内
COPY common /app/service_order/common
COPY communication /app/service_order/communication
COPY config /app/service_order/config
COPY handler /app/service_order/handler
COPY middleware /app/service_order/middleware
COPY nacos_client /app/service_order/nacos_client
COPY models /app/service_order/models
COPY locales /app/service_order/locales
COPY service_order /app/service_order

# 安装依赖
RUN pip install --no-cache-dir -r ./service_order/requirements.txt

# 设置 PYTHONPATH 环境变量，确保模块路径可访问
ENV PYTHONPATH=/app

# 暴露端口 (Robyn 默认端口是 5000，可以根据实际情况修改)
EXPOSE 8002

# 启动命令
CMD ["python", "service_order/app.py"]
