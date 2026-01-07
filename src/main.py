"""Main file."""

import logging

import streamlit as st

from config import (
    ENV,
    LLM_PROVIDERS,
    PAGE_ICON,
    SS_KEY_LLM_MODEL,
    SS_KEY_LLM_MODELS_LIST,
    SS_KEY_LLM_PROVIDER,
    SS_KEY_LLM_PROVIDER_INSTANCE,
    SS_KEY_LOGGED_IN,
)
from helper import (
    create_navigation,
    init_logging,
    show_login_page,
)
from llm import get_cached_llm_provider
from texts import (
    app_title,
    main_error_llm_provider,
    main_error_unexpected,
    main_info_check_config,
    main_llm_label,
    main_model_label,
)

# must be first Streamlit command
st.set_page_config(
    page_title=app_title,
    page_icon=PAGE_ICON,
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
    if ENV == "Prod" and not st.session_state.get(SS_KEY_LOGGED_IN, False):
        show_login_page()
        return

    _page = create_navigation()

    # Use key parameter for automatic session state binding
    st.sidebar.selectbox(
        main_llm_label,
        LLM_PROVIDERS,
        key=SS_KEY_LLM_PROVIDER,
        on_change=_clear_llm_cache,
    )

    # Get models list - cache for performance
    if SS_KEY_LLM_MODELS_LIST not in st.session_state:
        try:
            llm_provider = get_cached_llm_provider()
            st.session_state[SS_KEY_LLM_MODELS_LIST] = llm_provider.models
        except (ValueError, ConnectionError) as e:
            st.error(main_error_llm_provider.format(e))
            st.info(main_info_check_config)
            st.stop()
    models = st.session_state[SS_KEY_LLM_MODELS_LIST]

    # Use key parameter for automatic session state binding
    st.sidebar.selectbox(main_model_label, models, key=SS_KEY_LLM_MODEL)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        # Use st.error for production to avoid exposing stack traces
        if ENV == "Prod":
            st.error(main_error_unexpected)
        else:
            st.exception(e)
        st.stop()
