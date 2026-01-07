"""Main file."""

import logging

import streamlit as st

from config import (
    ENV,
    LLM_PROVIDERS,
    SS_KEY_LLM_MODEL,
    SS_KEY_LLM_MODELS_LIST,
    SS_KEY_LLM_PROVIDER,
    SS_KEY_LLM_PROVIDER_INSTANCE,
)
from helper import (
    create_navigation,
    init_logging,
    show_login_page,
)
from llm import get_cached_llm_provider

# must be first Streamlit command
st.set_page_config(
    page_title="Mind Chat",
    page_icon=":sun_behind_small_cloud:",
    layout="wide",
)

init_logging()
logger = logging.getLogger(__name__)


def _clear_llm_cache() -> None:
    """Clear all LLM-related cache from session state."""
    cache_keys = [
        SS_KEY_LLM_MODEL,
        SS_KEY_LLM_MODELS_LIST,
        SS_KEY_LLM_PROVIDER_INSTANCE,
    ]
    for key in cache_keys:
        if key in st.session_state:
            del st.session_state[key]


def main() -> None:  # noqa: D103
    # Login, only on prod
    if ENV == "Prod" and not st.session_state.get("logged_in", False):
        show_login_page()
        return

    _page = create_navigation()

    # LLM provider select
    if SS_KEY_LLM_PROVIDER not in st.session_state:
        st.session_state[SS_KEY_LLM_PROVIDER] = LLM_PROVIDERS[0]

    default_index = LLM_PROVIDERS.index(st.session_state[SS_KEY_LLM_PROVIDER])
    sel_provider = st.sidebar.selectbox(
        "LLM",
        LLM_PROVIDERS,
        index=default_index,
    )
    # Handle provider change
    if sel_provider != st.session_state[SS_KEY_LLM_PROVIDER]:
        st.session_state[SS_KEY_LLM_PROVIDER] = sel_provider
        _clear_llm_cache()
        st.rerun()

    # Get models list - cache for performance
    if SS_KEY_LLM_MODELS_LIST not in st.session_state:
        try:
            llm_provider = get_cached_llm_provider()
            st.session_state[SS_KEY_LLM_MODELS_LIST] = llm_provider.models
        except (ValueError, ConnectionError) as e:
            st.error(f"❌ LLM Provider Error: {e}")
            st.info(
                "💡 Please check your configuration or select a different provider."
            )
            st.stop()
    models = st.session_state[SS_KEY_LLM_MODELS_LIST]

    # Model select
    if SS_KEY_LLM_MODEL not in st.session_state:
        st.session_state[SS_KEY_LLM_MODEL] = models[0]

    default_index = models.index(st.session_state[SS_KEY_LLM_MODEL])
    sel_model = st.sidebar.selectbox("Modell", models, index=default_index)
    if sel_model != st.session_state[SS_KEY_LLM_MODEL]:
        st.session_state[SS_KEY_LLM_MODEL] = sel_model


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
