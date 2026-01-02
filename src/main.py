"""Main file."""

from pathlib import Path

import streamlit as st
from streamlit.logger import get_logger

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
    st.title("Mind Chat")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
