install:
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m unittest test_app.py

docker-build:
	docker build -t user-service .

docker-run:
	docker run -p 5000:5000 user-service

.PHONY: install run test docker-build docker-run
