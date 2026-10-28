#!/bin/sh
set -e
cd "$(dirname "$0")/.."

APP_ENV=Local uv run streamlit run src/main.py
# for production better use
# uv run python -O -m streamlit run src/main.py
