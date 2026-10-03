.PHONY: format check test test-coverage

format:
	uv run ruff check Main tests --fix --select I
	uv run ruff format Main tests

check:
	uv run ruff check Main tests
	uv run ruff format --diff Main tests
	uv run ty check Main tests
	uv lock --locked

test:
	uv run pytest -v --tb=short

test-coverage:
	uv run pytest -v --tb=short --cov --cov-report=xml
