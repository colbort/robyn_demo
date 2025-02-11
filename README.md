### 简介
    该项目是 robyn 框架搭建的 微服务项目
    中间件：
    1、mysql
    2、redis
    3、nacos （配置中心，服务注册和发现）
    4、rabbitmq 服务间通行
    5、traefik 网关
    6、限流
    7、内存缓存

### 运行和部署
```shell
git clone 
cd microservices-demo 
```

###### 部署
deploy 文件夹中有完整的 docker compose 部署方案；只需要修改 Makefile 中镜像地址既可完成打包镜像；部署可以直接使用 docker compose 完成