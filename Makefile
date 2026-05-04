.DEFAULT_GOAL := help
PYTHON := python3.12
UV := uv

.PHONY: help install install-dev sync lint format typecheck test test-cov clean pre-commit-install pre-commit-run build

# ── Setup ──────────────────────────────────────────────────────────────────────

help:
	@echo "vibe-spec dev commands"
	@echo ""
	@echo "  install            Install runtime dependencies"
	@echo "  install-dev        Install all dependencies including dev tools"
	@echo "  sync               Sync lockfile with pyproject.toml"
	@echo ""
	@echo "  lint               Run ruff linter"
	@echo "  format             Run ruff formatter"
	@echo "  typecheck          Run mypy"
	@echo "  test               Run pytest"
	@echo "  test-cov           Run pytest with coverage report"
	@echo ""
	@echo "  pre-commit-install Install pre-commit hooks"
	@echo "  pre-commit-run     Run all pre-commit hooks against staged files"
	@echo ""
	@echo "  clean              Remove build artifacts and caches"
	@echo "  build              Build distribution packages"

install:
	$(UV) sync --no-dev

install-dev:
	$(UV) sync --all-extras

sync:
	$(UV) lock

# ── Quality ────────────────────────────────────────────────────────────────────

lint:
	$(UV) run ruff check src/ tests/

format:
	$(UV) run ruff format src/ tests/
	$(UV) run ruff check --fix src/ tests/

typecheck:
	$(UV) run mypy src/

test:
	$(UV) run pytest tests/ -v

test-cov:
	$(UV) run pytest tests/ -v --cov=src/vibe_spec --cov-report=term-missing --cov-report=html

# ── Pre-commit ─────────────────────────────────────────────────────────────────

pre-commit-install:
	$(UV) run pre-commit install
	$(UV) run pre-commit install --hook-type commit-msg

pre-commit-run:
	$(UV) run pre-commit run --all-files

# ── Build ──────────────────────────────────────────────────────────────────────

build:
	$(UV) build

clean:
	rm -rf dist/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/ .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
