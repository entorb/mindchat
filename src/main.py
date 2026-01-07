"""Main file."""

import logging

import streamlit as st

from config import ENV, LLM_PROVIDERS
from helper import (
    create_navigation,
    init_logging,
    show_login_page,
)
from llm import get_llm_provider

# must be first Streamlit command
st.set_page_config(
    page_title="Mind Chat",
    page_icon=":sun_behind_small_cloud:",
    layout="wide",
)

init_logging()
logger = logging.getLogger(__name__)


def main() -> None:  # noqa: D103
    # Login, only on prod
    if ENV == "Prod" and not st.session_state.get("logged_in", False):
        show_login_page()
        return

    _page = create_navigation()

    # LLM provider select
    if "LLM_PROVIDER" not in st.session_state:
        st.session_state["LLM_PROVIDER"] = LLM_PROVIDERS[0]

    default_index = LLM_PROVIDERS.index(st.session_state["LLM_PROVIDER"])
    sel_provider = st.sidebar.selectbox(
        "LLM",
        LLM_PROVIDERS,
        index=default_index,
    )
    # Handle provider change
    if sel_provider != st.session_state["LLM_PROVIDER"]:
        st.session_state["LLM_PROVIDER"] = sel_provider
        del st.session_state["LLM_MODEL"]
        st.rerun()

    llm_provider = get_llm_provider(provider=st.session_state["LLM_PROVIDER"])
    models = llm_provider.models

    # Model select
    if "LLM_MODEL" not in st.session_state:
        st.session_state["LLM_MODEL"] = models[0]

    default_index = models.index(st.session_state["LLM_MODEL"])
    sel_model = st.sidebar.selectbox("Modell", models, index=default_index)
    if sel_model != st.session_state["LLM_MODEL"]:
        st.session_state["LLM_MODEL"] = sel_model
    del sel_provider, sel_model, default_index, models


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
