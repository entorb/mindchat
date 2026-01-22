"""Configuration."""

from pathlib import Path
from zoneinfo import ZoneInfo

PATH_PROD_CHECK = Path("/var/www/virtual/entorb/html")
PATH_WEBSTATS_SCRIPT = "/var/www/virtual/entorb/web-stats.py"
PATH_SD_TEMPLATE = Path("src/prompts/self-disclosure-template.md")
PATH_PAGE_SELF = Path("reports/r01_self.py")
PATH_PAGE_CHAT = Path("reports/r02_chat.py")
PATH_PAGE_LOGOUT = Path("reports/r99_logout.py")


# Session state keys
SS_KEY_CHAT_HISTORY = "chat_history"
SS_KEY_LLM_MODEL = "LLM_MODEL"
SS_KEY_LLM_MODELS_LIST = "_llm_models_list"
SS_KEY_LLM_PROVIDER = "LLM_PROVIDER"
SS_KEY_LLM_PROVIDER_INSTANCE = "_llm_provider_instance"
SS_KEY_LOGGED_IN = "logged_in"
SS_KEY_SD = "my-self-disclosure"

ENV = "Prod" if PATH_PROD_CHECK.exists() else "Local"

if ENV == "Prod":
    LLM_PROVIDERS = ["OpenAI"]
else:
    LLM_PROVIDERS = ["Ollama", "OpenAI", "Mistral", "Google"]


# Page configuration
PAGE_ICON = ":sun_behind_small_cloud:"

TIMEZONE = ZoneInfo("Europe/Berlin")
