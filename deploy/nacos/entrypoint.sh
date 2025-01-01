#!/bin/bash
# entrypoint.sh

echo "开始启动 Nacos"
echo "NACOS_USERNAME: $NACOS_USERNAME"
echo "NACOS_PASSWORD: $NACOS_PASSWORD"
echo "NACOS_NAMESPACE: $NACOS_NAMESPACE"

sleep 5

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

# 使用默认用户名和密码登录，获取 Token
echo "登录 Nacos 并获取 Token..."
# 发送 POST 请求，捕获返回值和 HTTP 状态码
response=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:8848/nacos/v1/auth/users/admin" \
    -d "username=$NACOS_USERNAME" \
    -d "password=$NACOS_PASSWORD")

# 分离返回值和 HTTP 状态码
response_body=$(echo "$response" | sed '$d')  # 去掉最后一行 (HTTP 状态码)
http_code=$(echo "$response" | tail -n 1)    # 取最后一行 (HTTP 状态码)

# 输出接口返回值和状态码
echo "接口返回 HTTP 状态码: $http_code"
echo "接口返回数据: $response_body"

# 根据状态码判断成功与否
if [ "$http_code" -eq 200 ]; then
    echo "初始化用户名密码成功"
else
    echo "初始化用户名密码失败，HTTP 状态码: $http_code"
    exit 1
fi

response=$(curl -s -X POST 'http://localhost:8848/nacos/v1/auth/login' \
  -d "username=nacos" \
  -d "password=$NACOS_PASSWORD")

echo "获取token  $response"
token=$(echo $response | jq -r '.accessToken')
# 检查 Token 是否获取成功
if [ -z "$token" ] || [ "$token" == "null" ]; then
  echo "获取 Token 失败，请检查用户名或密码！"
  exit 1
fi
echo "Access Token: $token"

# 读取配置文件内容
content=$(cat /home/init/mall.yaml)

# 查询命名空间
response=$(curl -s -X GET "http://localhost:8848/nacos/v2/console/namespace/list" \
    -H "Authorization: Bearer $token")
# 使用 jq 解析返回的 JSON 数据，检查命名空间是否存在
namespaceExists=$(echo "$response" | jq -r --arg NAMESPACE "$NACOS_NAMESPACE" '.data[] | select(.namespace == $NAMESPACE) | .namespace')

if [ "$namespaceExists" == "$NACOS_NAMESPACE" ]; then
    echo "命名空间 '$NACOS_NAMESPACE' 已存在"
else
  # 创建命名空间并捕获 namespaceId
  response=$(curl -s -X POST "http://localhost:8848/nacos/v2/console/namespace" \
      -H "Authorization: Bearer $token" \
      -d "namespaceId=$NACOS_NAMESPACE" \
      -d "namespaceName=$NACOS_NAMESPACE")

  # 检查命名空间创建状态
  echo "创建命名空间 $response"
  if echo "$response" | grep -q '"code":0'; then
      echo "命名空间 '$NACOS_NAMESPACE' 创建成功"
  else
      echo "命名空间创建失败，返回信息：$response"
      exit 1
  fi
fi

# 3. 导入配置文件到指定命名空间
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8848/nacos/v2/cs/config" \
    -H "Authorization: Bearer $token" \
    -d "dataId=mall.yaml" \
    -d "group=DEFAULT_GROUP" \
    -d "namespaceId=$NACOS_NAMESPACE" \
    -d "type=yaml" \
    --data-urlencode "content=$content")

# 检查配置导入状态
if [ "$response" -eq 200 ]; then
    echo "配置文件导入成功"
else
    echo "配置文件导入失败，HTTP 状态码: $response"
fi


# 保持容器运行
tail -f /dev/null

