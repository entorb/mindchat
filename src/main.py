"""Main file."""

import time
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st
from streamlit.logger import get_logger

from helper import (
    init_matomo,
    init_sentry,
)

if TYPE_CHECKING:
    from streamlit.navigation.page import StreamlitPage

# must be first Streamlit command
st.set_page_config(
    page_title="Mind Chat",
    page_icon=":sun_behind_small_cloud:",
    layout="wide",
)

# running on webserver?
if Path("/var/www/virtual/entorb/html").exists():
    # TODO: fix
    if 1 == 2:  # noqa: PLR0133
        init_sentry()
    init_matomo()


logger = get_logger(__file__)


def show_login_page() -> None:
    """Display login page and handle authentication."""
    st.title("Login")
    st.write("Frage Torben nach dem Geheimnis.")

    input_password = st.text_input(
        "Geheimnis", type="password", key="login_password_input"
    )

    if st.button("Anmelden") or input_password:
        if input_password == st.secrets["login_password"]:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            time.sleep(3)  # Mitigate brute-force attacks
            st.warning("Falsch!")


def main() -> None:  # noqa: D103
    # Check if user is logged in
    if not st.session_state.get("logged_in", False):
        show_login_page()
        return

    # create_navigation_menu
    lst: list[StreamlitPage] = []
    lst.append(st.Page(page="reports/r00_info.py", title="Info"))
    lst.append(st.Page(page="reports/r01_self.py", title="Selbstauskunft"))
    lst.append(st.Page(page="reports/r02_chat.py", title="Chat"))
    lst.append(st.Page(page="reports/r99_logout.py", title="Logout"))
    pg = st.navigation(pages=lst, position="sidebar", expanded=True)
    pg.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
