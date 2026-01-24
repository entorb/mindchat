#!/bin/sh

# ensure we are in the root dir
cd $(dirname $0)/..

# exit upon error
set -e

uv remove numpy pandas pyarrow streamlit google-genai mistralai openai pydantic
uv remove --dev ruff pre-commit pytest pytest-cov tomli-w watchdog ollama

uv lock --upgrade
uv sync --upgrade

# pin to old versions due to Uberspace restrictions
uv add numpy==2.2.3 pandas==2.2.3 pyarrow==20.0.0 streamlit google-genai mistralai openai pydantic
uv add --dev ruff pre-commit pytest pytest-cov tomli-w watchdog ollama

uv lock --upgrade
uv sync --upgrade

python scripts/gen_requirements.py

echo DONE
