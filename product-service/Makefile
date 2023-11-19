# Makefile for the Flask Product Service

# Variables
DOCKER_IMAGE_NAME=wine-store-product-service
DOCKER_CONTAINER_NAME=wine-store-product-service-container

# Install Python dependencies
install:
	pip install -r requirements.txt

# Run the Flask app
run:
	FLASK_APP=app.py FLASK_ENV=development flask run

# Run tests
test:
	python test_app.py

# Build the Docker image
docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Docker container
docker-run: docker-build
	docker run --name $(DOCKER_CONTAINER_NAME) -p 5000:5000 -d $(DOCKER_IMAGE_NAME)

# Stop and remove the Docker container
docker-stop:
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)

# Run the Docker container interactively (useful for debugging)
docker-run-interactive: docker-build
	docker run --name $(DOCKER_CONTAINER_NAME) -p 5000:5000 -it $(DOCKER_IMAGE_NAME) /bin/bash

.PHONY: install run test docker-build docker-run docker-stop docker-run-interactive
