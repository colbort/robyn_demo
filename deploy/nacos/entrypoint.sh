#!/bin/bash
# entrypoint.sh

echo "开始启动 Nacos"

# 启动 Nacos并放入后台
/home/nacos/bin/docker-startup.sh -m standalone &

# 等待 Nacos 完全启动
while ! curl -s "http://localhost:8848/nacos/v1/ns/operator/metrics" | grep "\"status\":\"UP\""; do
    echo "等待 Nacos 启动..."
    sleep 2
done

echo "Nacos 启动完成"

apk update
apk add jq

token_response=$(curl -s -X POST 'http://localhost:8848/nacos/v1/auth/login' \
  -d 'username=nacos' \
  -d 'password=123456')

echo "获取token  $response"
token=$(echo $token_response | jq -r '.accessToken')
# 检查 Token 是否获取成功
if [ -z "$token" ] || [ "$token" == "null" ]; then
  echo "获取 Token 失败，请检查用户名或密码！"
  exit 1
fi
echo "Access Token: $token"

# 读取配置文件内容
content=$(cat /home/init/mall.yaml)

echo "导入配置内容：\n${content}\n"

NAMESPACE="mall"

# 发起 POST 请求创建 namespace
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST 'http://localhost:8848/nacos/v1/console/namespaces' \
     -H "Authorization: Bearer $token" \
     -d "customNamespaceId=$NAMESPACE" \
     -d "namespaceName=$NAMESPACE" \
     -d "namespaceDesc=")

# 检查响应状态码是否为 200
if [ "$response" -eq 200 ]; then
    echo "Namespace 创建成功"
else
    echo "创建 Namespace 失败，HTTP 状态码: $response"
fi

# 使用 Nacos API 导入配置，指定 dataId 和 group
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8848/nacos/v1/cs/configs" \
     -H "Authorization: Bearer $token" \
     -d "dataId=mall.yaml" \
     -d "group=DEFAULT_GROUP" \
     -d "namespaceId=$NAMESPACE" \
     -d "type=yaml" \
     --data-urlencode "content=$content")
# 检查响应状态码是否为 200
if [ "$response" -eq 200 ]; then
    echo "配置文件导入成功"
else
    echo "配置文件导入失败，HTTP 状态码: $response"
fi

# 保持容器运行
tail -f /dev/null

