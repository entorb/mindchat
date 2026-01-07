"""Configuration."""

from pathlib import Path

PROD_PATH = Path("/var/www/virtual/entorb/html")
WEBSTATS_SCRIPT = "/var/www/virtual/entorb/web-stats.py"
SD_TEMPLATE_PATH = Path("src/prompts/self-disclosure-template.md")


# Session state keys
SS_KEY_CHAT_HISTORY = "chat_history"
SS_KEY_LLM_MODEL = "LLM_MODEL"
SS_KEY_LLM_MODELS_LIST = "_llm_models_list"
SS_KEY_LLM_PROVIDER = "LLM_PROVIDER"
SS_KEY_LLM_PROVIDER_INSTANCE = "_llm_provider_instance"
SS_KEY_LOGGED_IN = "logged_in"
SS_KEY_SD = "my-self-disclosure"

ENV = "Prod" if PROD_PATH.exists() else "Local"

if ENV == "Prod":
    LLM_PROVIDERS = ["OpenAI"]
else:
    LLM_PROVIDERS = ["Ollama", "OpenAI", "Mistral", "Google"]


# Page configuration
PAGE_ICON = ":sun_behind_small_cloud:"
