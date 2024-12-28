# 镜像仓库命名空间
IMAGE_NAME          = mall_python
# 镜像地址
REPOSITORY          = docker.live168.xyz/${IMAGE_NAME}
# 镜像版本
VERSION=1.0.0


build_core:
	@SERVICE_DIR=service_core; \
    (cd $$SERVICE_DIR && pwd && ./build.sh); \
    docker build --platform linux/amd64 --build-arg LOCALES_DIR=locales \
    -t $$SERVICE_DIR -f $$SERVICE_DIR/Dockerfile .; \
    docker tag $$SERVICE_DIR ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi $$SERVICE_DIR


build_user:
	@SERVICE_DIR=service_user; \
    (cd $$SERVICE_DIR && pwd && ./build.sh); \
    docker build --platform linux/amd64 --build-arg LOCALES_DIR=locales \
    -t $$SERVICE_DIR -f $$SERVICE_DIR/Dockerfile .; \
    docker tag $$SERVICE_DIR ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi $$SERVICE_DIR


build_order:
	@SERVICE_DIR=service_order; \
    (cd $$SERVICE_DIR && pwd && ./build.sh); \
    docker build --platform linux/amd64 --build-arg LOCALES_DIR=locales \
    -t $$SERVICE_DIR -f $$SERVICE_DIR/Dockerfile .; \
    docker tag $$SERVICE_DIR ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi $$SERVICE_DIR


build_product:
	@SERVICE_DIR=service_product; \
    (cd $$SERVICE_DIR && pwd && ./build.sh); \
    docker build --platform linux/amd64 --build-arg LOCALES_DIR=locales \
    -t $$SERVICE_DIR -f $$SERVICE_DIR/Dockerfile .; \
    docker tag $$SERVICE_DIR ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi $$SERVICE_DIR


build_wallet:
	@SERVICE_DIR=service_wallet; \
    (cd $$SERVICE_DIR && pwd && ./build.sh); \
    docker build --platform linux/amd64 --build-arg LOCALES_DIR=locales \
    -t $$SERVICE_DIR -f $$SERVICE_DIR/Dockerfile .; \
    docker tag $$SERVICE_DIR ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);\
    docker rmi $$SERVICE_DIR


build: build_core build_user build_order build_product build_wallet