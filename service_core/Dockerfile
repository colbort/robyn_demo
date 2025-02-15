# 使用 Python 3.10 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 定义变量，设置 service_core 的路径
ARG SERVICE_PATH=/app/service_core

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
COPY cache $SERVICE_PATH/cache
COPY common $SERVICE_PATH/common
COPY communication $SERVICE_PATH/communication
COPY config $SERVICE_PATH/config
COPY errors $SERVICE_PATH/errors
COPY handler $SERVICE_PATH/handler
COPY middleware $SERVICE_PATH/middleware
COPY nacos_client $SERVICE_PATH/nacos_client
COPY models $SERVICE_PATH/models
COPY locales $SERVICE_PATH/locales
COPY service_core $SERVICE_PATH

# 安装依赖
RUN pip install --no-cache-dir -r ./service_core/requirements.txt

# 设置 PYTHONPATH 环境变量，确保模块路径可访问
ENV PYTHONPATH=/app

# 暴露端口 (Robyn 默认端口是 5000，可以根据实际情况修改)
EXPOSE 8000

# 启动命令
CMD ["python", "service_core/app.py"]
