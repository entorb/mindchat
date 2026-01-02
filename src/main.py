"""Main file."""

from pathlib import Path

import streamlit as st
from streamlit.logger import get_logger
from streamlit.navigation.page import StreamlitPage

from helper import (
    init_matomo,
    init_sentry,
)

# must be first Streamlit command
st.set_page_config(
    page_title="Mind Chat",
    page_icon=":sun_behind_small_cloud:",
    layout="wide",
)

# running on webserver?
if Path("/var/www/virtual/entorb/html").exists():
    init_sentry()
    init_matomo()


logger = get_logger(__file__)


def main() -> None:  # noqa: D103
    # create_navigation_menu
    lst: list[StreamlitPage] = []
    lst.append(st.Page(page="reports/r00_disclaimer.py", title="Disclaimer"))
    lst.append(st.Page(page="reports/r01_self.py", title="Selbstauskunft"))
    lst.append(st.Page(page="reports/r02_chat.py", title="Chat"))
    lst.append(st.Page(page="reports/r99_logout.py", title="Logout"))
    pg = st.navigation(lst)
    pg.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
