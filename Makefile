.PHONY: build run stop logs

# 镜像仓库命名空间
IMAGE_NAME          = mall_python
# 镜像地址
REPOSITORY          = docker.live168.xyz/${IMAGE_NAME}
# 镜像版本
VERSION=v1.0.6

build_core:
	@SERVICE_DIR=service_core; \
    docker buildx build --platform linux/arm64 \
    -t ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) -f $$SERVICE_DIR/Dockerfile --load .; \
    docker tag ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);

build_user:
	@SERVICE_DIR=service_user; \
	docker buildx build --platform linux/arm64 \
    -t ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) -f $$SERVICE_DIR/Dockerfile --load .; \
    docker tag ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);

build_order:
	@SERVICE_DIR=service_order; \
	docker buildx build --platform linux/arm64 \
    -t ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) -f $$SERVICE_DIR/Dockerfile --load .; \
    docker tag ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);

build_product:
	@SERVICE_DIR=service_product; \
	docker buildx build --platform linux/arm64 \
    -t ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) -f $$SERVICE_DIR/Dockerfile --load .; \
    docker tag ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);

build_wallet:
	@SERVICE_DIR=service_wallet; \
	docker buildx build --platform linux/arm64 \
    -t ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) -f $$SERVICE_DIR/Dockerfile --load .; \
    docker tag ${REPOSITORY}/$$SERVICE_DIR:$(VERSION) ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker push ${REPOSITORY}/$$SERVICE_DIR:$(VERSION); \
    docker rmi ${REPOSITORY}/$$SERVICE_DIR:$(VERSION);


build: build_core build_user build_order build_product build_wallet