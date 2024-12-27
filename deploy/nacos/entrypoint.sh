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
apt update
apt-get install -y jq

# 读取配置文件内容
content=$(cat /home/init/mall.yaml)

echo "导入配置内容：\n${content}\n"

## 发起 POST 请求创建 namespace
#response=$(curl -s -o /dev/null -w "%{http_code}" -X POST 'http://localhost:8848/nacos/v1/console/namespaces' \
#     -d 'customNamespaceId=' \
#     -d 'namespaceName=prod' \
#     -d 'namespaceDesc=')
#
## 检查响应状态码是否为 200
#if [ "$response" -eq 200 ]; then
#    echo "Namespace 'prod' 创建成功"
#else
#    echo "创建 Namespace 'prod' 失败，HTTP 状态码: $response"
#fi
#
## 发送请求获取 namespace 列表
#response=$(curl -s -X GET 'http://localhost:8848/nacos/v1/console/namespaces')
#
## 使用 jq 解析 JSON，并查找 namespaceShowName 为 "prod" 的 namespace ID
#namespaceId=$(echo "$response" | jq -r '.data[] | select(.namespaceShowName == "prod") | .namespace')
#
## 检查是否获取到 namespaceId
#if [ -z "$namespaceId" ]; then
#    echo "未找到 namespace 为 'prod' 的 ID"
#else
#    echo "namespace ID for 'prod' is: $namespaceId"
#fi

# 使用 Nacos API 导入配置，指定 dataId 和 group
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8848/nacos/v1/cs/configs" \
     -d "dataId=yunwei.properties" \
     -d "group=DEFAULT_GROUP" \
     -d "type=properties" \
     --data-urlencode "content=$content")
# 检查响应状态码是否为 200
if [ "$response" -eq 200 ]; then
    echo "配置文件导入成功"
else
    echo "配置文件导入失败，HTTP 状态码: $response"
fi

# 保持容器运行
tail -f /dev/null

