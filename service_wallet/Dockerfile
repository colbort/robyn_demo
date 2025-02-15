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
COPY cache /app/service_wallet/cache
COPY common /app/service_wallet/common
COPY communication /app/service_wallet/communication
COPY config /app/service_wallet/config
COPY handler /app/service_wallet/handler
COPY middleware /app/service_wallet/middleware
COPY nacos_client /app/service_wallet/nacos_client
COPY models /app/service_wallet/models
COPY locales /app/service_wallet/locales
COPY service_wallet /app/service_wallet

# 安装依赖
RUN pip install --no-cache-dir -r ./service_wallet/requirements.txt

# 设置 PYTHONPATH 环境变量，确保模块路径可访问
ENV PYTHONPATH=/app

# 暴露端口 (Robyn 默认端口是 5000，可以根据实际情况修改)
EXPOSE 8004

# 启动命令
CMD ["python", "service_wallet/app.py"]
