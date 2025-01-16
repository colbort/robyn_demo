#!/bin/sh

LOG_FILE="/var/log/nacos_healthcheck.log"

echo "NACOS_USERNAME: $NACOS_USERNAME" | tee -a $LOG_FILE
echo "NACOS_PASSWORD: $NACOS_PASSWORD" | tee -a $LOG_FILE

# 获取 Token
token=$(curl -s -X POST "http://localhost:8848/nacos/v1/auth/login" \
        -d "username=$NACOS_USERNAME" \
        -d "password=$NACOS_PASSWORD" | jq -r '.accessToken')

# 检查 Token 是否有效
if [ -z "$token" ] || [ "$token" = "null" ]; then
  echo "Failed to get token" | tee -a $LOG_FILE
  exit 1
fi

# 请求 Nacos 配置数据
response=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $token" \
           "http://localhost:8848/nacos/v2/cs/config?dataId=mall.yaml&group=DEFAULT_GROUP&namespaceId=mall")

# 判断 HTTP 响应状态码
if [ "$response" -eq 200 ]; then
  echo "Healthcheck passed" | tee -a $LOG_FILE
  exit 0
else
  echo "Healthcheck failed, HTTP code: $response" | tee -a $LOG_FILE
  exit 1
fi
