"""Configuration."""

import os
from getpass import getuser
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

PATH_WEBSTATS_SCRIPT = Path("/var/www/virtual") / getuser() / "web-stats.py"
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

# unset defaults to PROD: fail safe, login required
_APP_ENV = os.environ.get("APP_ENV", "PROD")
if _APP_ENV not in ("PROD", "Local"):
    msg = f"Invalid APP_ENV: {_APP_ENV!r}, expected 'PROD' or 'Local'"
    raise ValueError(msg)
ENV: Literal["PROD", "Local"] = "PROD" if _APP_ENV == "PROD" else "Local"

if ENV == "PROD":
    LLM_PROVIDERS = ["Mistral"]
else:
    LLM_PROVIDERS = ["Ollama", "Mistral", "OpenAI", "Google"]


# Page configuration
PAGE_ICON = ":sun_behind_small_cloud:"

TIMEZONE = ZoneInfo("Europe/Berlin")
