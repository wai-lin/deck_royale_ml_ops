CODE_DIRS = src/ tests/

install:
	@echo "Installing dependencies..."
	uv sync
	uv run pre-commit install
	@echo "Pre-commit hooks installed."

dev: ## Run the FastAPI application
	@echo "Running FastAPI application..."
	uv run uvicorn src.main:app --reload

format: ## Format code using Ruff formatter
	@echo "Formatting code..."
	uv run ruff format $(CODE_DIRS)

format-check: ## Check if code is formatted correctly (for CI)
	@echo "Checking code formatting..."
	uv run ruff format --check $(CODE_DIRS)

lint: ## Check for linting issues using Ruff (no fixes)
	@echo "Linting code..."
	uv run ruff check $(CODE_DIRS)

lint-fix: ## Attempt to automatically fix linting issues using Ruff
	@echo "Attempting to fix linting issues..."
	uv run ruff check --fix $(CODE_DIRS)

autofix: lint-fix format ## Automatically fix linting issues and then format code
	@echo "Code auto-fixing and formatting complete."

type-check: ## Run mypy type checking separately
	uv run mypy src/ --config-file=pyproject.toml

check-all: lint format-check type-check test pre-commit ## Run all checks (lint + test)
	@echo "All checks complete."

test: ## Run tests using pytest
	@echo "Running tests..."
	uv run python -m pytest
	@echo "Tests completed."
