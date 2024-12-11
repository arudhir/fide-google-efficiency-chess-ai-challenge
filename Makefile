.PHONY: \
	help \
	test profile submit \
	clean clean-build clean-pyc \
	dist image up down bash

# --- Environment---
# use Bash with brace expansion
.SHELLFLAGS = -cB
SHELL = /bin/bash
PROJECT_SLUG = chess-bot
BUILD_IMAGE ?= $(PROJECT_SLUG)
DOCKER_REGISTRY ?= docker.arudhir.com

help:
	@echo
	@echo "Usage: make [target]"
	@echo
	@echo "Cleanup:"
	@echo "    clean              clean build artifacts and Python cache"
	@echo "    clean-build        remove build artifacts"
	@echo "    clean-pyc          remove Python file artifacts"
	@echo
	@echo "Testing:"
	@echo "    test               run basic tests"
	@echo
	@echo "Submission:"
	@echo "    submit             create and submit to Kaggle"
	@echo "    dist               create submission archive"
	@echo
	@echo "Docker:"
	@echo "    image              build Docker image"
	@echo "    up                 start containers"
	@echo "    down               stop containers"
	@echo "    bash               start bash in container"
	@echo "    tag                tag Docker image"
	@echo "    push               push to registry"
	@echo

# --- Python ---
venv:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

test:
	uv run pytest tests -v -s

# --- Cleanup ---
clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -f submission.tar.gz

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# --- Submission ---
dist:
	tar -czf submission.tar.gz submission

submit: dist
	kaggle competitions submit \
		-c fide-google-efficiency-chess-ai-challenge \
		-f submission.tar.gz \
		-m $(message)


# Default message if none provided
message ?= "default"

# --- Docker ---
image:
	docker-compose build
	@echo "Built $(BUILD_IMAGE) image"

up:
	docker-compose up -d
	@echo "Started containers"

down:
	docker-compose down
	@echo "Stopped containers"

bash:
	docker-compose run --rm $(PROJECT_SLUG) bash

tag: image
	docker tag $(BUILD_IMAGE) $(DOCKER_REGISTRY)/$(BUILD_IMAGE)
	@echo "Tagged image as $(DOCKER_REGISTRY)/$(BUILD_IMAGE)"

push: tag
	docker push $(DOCKER_REGISTRY)/$(BUILD_IMAGE)
	@echo "Pushed image to registry"

# --- Testing with Stockfish ---
test-stockfish: up
	docker-compose run --rm $(PROJECT_SLUG) python stockfish_test.py