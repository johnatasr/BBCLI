.PHONY: tests lint

tests:
	pytest

lint:
	isort app
	black app
