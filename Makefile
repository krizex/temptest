SERVICE := xs-agent
IMAGE_LABEL := krizex/xs-agent

CONTAINER_PORT := 8000
HOST_PORT := 8002
CUR_DIR := $(shell pwd)
APP_CONTAINER_NAME := $(SERVICE)
APP_CONTAINER_HOST_NAME := $(SERVICE)
MQ_CONTAINER_NAME := xs-mq
MQ_PORT := 1080

.PHONY: build
build:
	docker build -t $(IMAGE_LABEL) .

.PHONY: debug
debug:
	docker run -it --rm \
	--hostname $(APP_CONTAINER_HOST_NAME) \
	--link $(MQ_CONTAINER_NAME) \
	-p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) \
	--env-file mq.env \
	-p $(HOST_PORT):$(CONTAINER_PORT) \
	-v /etc/localtime:/etc/localtime:ro \
	-v $(CUR_DIR)/src:/opt/xs-agent/app:rw \
	--security-opt seccomp:unconfined \
	$(IMAGE_LABEL):latest /bin/bash

.PHONY: run stop restart attach

run:
	docker run --rm -d \
	--hostname $(APP_CONTAINER_HOST_NAME) \
	--name $(APP_CONTAINER_NAME) \
	-p $(HOST_PORT):$(CONTAINER_PORT) \
	$(IMAGE_LABEL):latest

attach:
	docker exec -it $(APP_CONTAINER_NAME) /bin/bash

stop:
	docker stop $(APP_CONTAINER_NAME)

restart: stop run


.PHONY: push pull
push:
	docker push ${IMAGE_LABEL}

pull:
	docker pull ${IMAGE_LABEL}

.PHONY: run-mq stop-mq
run-mq:
	docker run --rm -d --name $(MQ_CONTAINER_NAME) --env-file mq.env -p $(MQ_PORT):5672 rabbitmq

stop-mq:
	docker stop $(MQ_CONTAINER_NAME)



##################


# .PHONY: run stop restart attach
# run:
# 	docker-compose up -d
# attach:
# 	docker exec -it $(APP_CONTAINER_NAME) /bin/bash
# stop:
# 	docker-compose down
# restart: stop run
