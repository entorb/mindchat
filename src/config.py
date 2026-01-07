"""Configuration."""

from pathlib import Path

PROD_PATH = Path("/var/www/virtual/entorb/html")
WEBSTATS_SCRIPT = "/var/www/virtual/entorb/web-stats.py"

SD_KEY = "my-self-disclosure"

ENV = "Prod" if PROD_PATH.exists() else "Local"

if ENV == "Prod":
    LLM_PROVIDERS = ["OpenAI"]
else:
    LLM_PROVIDERS = ["Ollama", "OpenAI", "Mistral", "Google"]

SPINNER_MESSAGES = [
    "Magic happens…",
    "Schmelze Gletscher…",
    "Falte Raum, Zeit und Tokens…",
    "Zeit zum Durchatmen…",
]
