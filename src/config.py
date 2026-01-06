"""Configuration."""

from pathlib import Path

PROD_PATH = Path("/var/www/virtual/entorb/html")
WEBSTATS_SCRIPT = "/var/www/virtual/entorb/web-stats.py"

ENV = "Prod" if PROD_PATH.exists() else "Local"

if ENV == "Prod":
    LLM_PROVIDER = "OpenAI"
    LLM_MODEL = "gpt-5-mini"  # gpt-5-nano, gpt-5-mini, gpt-5
if ENV == "Ollama":
    LLM_PROVIDER = "Ollama"
    LLM_MODEL = "mistral"  # mistral, llama3.2
if ENV == "Mistral":
    LLM_PROVIDER = "Mistral"
    LLM_MODEL = "mistral-medium-latest"
else:
    LLM_PROVIDER = "Ollama"
    LLM_MODEL = "mistral"  # mistral, llama3.2

SPINNER_MESSAGES = [
    "Magic happens…",
    "Schmelze Gletscher…",
    "Falte Raum, Zeit und Tokens…",
    "Zeit zum Durchatmen…",
]
