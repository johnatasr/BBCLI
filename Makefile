.PHONY: tests lint

tests:
	pytest

lint:
	flake8 app
	isort app
	black app
