install:
	poetry install

build: install
	poetry build

test: build
	poetry run pytest tests

lint: build
	poetry run pylint honeycomb tests

.PHONY: install build test lint

# example:
# 	cd ./examples/hello-world-flask && poetry run flask run

example:
	cd ./examples/hello-world-flask && \
	poetry install && \
	poetry run opentelemetry-instrument flask run
