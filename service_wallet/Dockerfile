# 使用一个轻量级的基础镜像
FROM debian:bullseye-slim

# 创建工作目录
WORKDIR /app

# 复制可执行文件到容器
COPY dist/app /app/
COPY ../locales /app/

# 设置运行时环境变量（可选）
ENV APP_ENV=prod

# 暴露端口（根据需求）
EXPOSE 8004

# 设置默认启动命令
CMD ["./app"]
