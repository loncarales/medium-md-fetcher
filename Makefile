all: help

.PHONY: uv
uv: ## Sync uv
	@echo "Synchronizing uv ..."
	@uv sync

.PHONY: format
format: ## Run ruff formatter
	 @echo "Running ruff formatter..."
	 @uv run ruff format .

.PHONY: lint
lint: ## Run ruff linter
	 @echo "Running ruff linter..."
	 @uv run ruff check . --fix

.PHONY: run
run: ## Run the application
	@echo "Running the application..."
	@uv run python medium.py

.PHONY: test
test: ## Run tests
	@echo "Running tests..."
	@uv run coverage run -m pytest tests/ -v

.PHONY: coverage
coverage: ## Show code coverage
	@echo "Show code coverage ..."
	@uv run coverage report -m

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
