"""Main file."""

import logging

import streamlit as st

from config import ENV
from helper import (
    create_navigation,
    init_logging,
    init_matomo,
    init_sentry,
    show_login_page,
)

# must be first Streamlit command
st.set_page_config(
    page_title="Mind Chat",
    page_icon=":sun_behind_small_cloud:",
    layout="wide",
)

init_logging()
logger = logging.getLogger(__name__)


def main() -> None:  # noqa: D103
    # Only if running on webserver
    if ENV == "Prod":
        init_sentry()
        init_matomo()

    # Check if user is logged in
    if ENV == "Prod" and not st.session_state.get("logged_in", False):
        show_login_page()
        return

    _page = create_navigation()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
