install:
	poetry install

build: install
	poetry build

test: build
	poetry run pytest tests

lint: build
	poetry run pylint honeycomb tests

.PHONY: install build test lint
