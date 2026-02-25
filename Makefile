.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make up      - Start the development environment (Docker)"
	@echo "  make down    - Stop the development environment"
	@echo "  make deploy  - Deploy Vespa application package"
	@echo "  make test    - Run all tests with coverage"
	@echo "  make lint    - Run ruff for linting and formatting"

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: deploy
deploy:
	uv run deploy-vespa

.PHONY: test
test:
	uv run pytest

.PHONY: lint
lint:
	uv run ruff check .
	uv run ruff format .
