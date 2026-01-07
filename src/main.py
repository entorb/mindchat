"""Main file."""

import logging

import streamlit as st

from config import (
    ENV,
    PAGE_ICON,
    SS_KEY_LOGGED_IN,
)
from helper import (
    create_navigation,
    init_logging,
    llm_select_in_sidebar,
    show_login_page,
    version_date_in_sidebar,
)
from texts import (
    app_title,
    main_error_unexpected,
)

# must be first Streamlit command
st.set_page_config(
    page_title=app_title,
    page_icon=PAGE_ICON,
    layout="wide",
)

init_logging()
LOGGER = logging.getLogger(__name__)


def main() -> None:  # noqa: D103
    # Login, only on prod
    if ENV == "Prod" and not st.session_state.get(SS_KEY_LOGGED_IN, False):
        show_login_page()
        return

    page = create_navigation()
    page.run()
    version_date_in_sidebar()
    llm_select_in_sidebar()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        LOGGER.exception("Exception:")
        # Use st.error for production to avoid exposing stack traces
        if ENV == "Prod":
            st.error(main_error_unexpected)
        else:
            st.exception(e)
        st.stop()
