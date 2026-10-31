#!/bin/sh
set -e
cd "$(dirname "$0")/.."

uv remove streamlit google-genai mistralai openai pydantic
uv remove --dev ruff pytest pytest-cov tomli-w watchdog ollama

uv lock --upgrade
uv sync --upgrade

# pin to old versions due to Uberspace restrictions
uv add streamlit google-genai mistralai openai pydantic
uv add --dev ruff pytest pytest-cov tomli-w watchdog ollama

uv lock --upgrade
uv sync --upgrade

python scripts/gen_requirements.py

# ruff
uv run ruff format
uv run ruff check --fix

# pre-commit
prek autoupdate --cooldown-days 7
prek run --all-files

echo DONE
