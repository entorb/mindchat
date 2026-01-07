"""Helper Functions."""

import datetime as dt
import logging
import subprocess
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from config import (
    LLM_PROVIDERS,
    SS_KEY_LLM_MODEL,
    SS_KEY_LLM_MODELS_LIST,
    SS_KEY_LLM_PROVIDER,
    SS_KEY_LLM_PROVIDER_INSTANCE,
    SS_KEY_LOGGED_IN,
    WEBSTATS_SCRIPT,
)
from llm import get_cached_llm_provider
from texts import (
    app_title,
    login_btn_label,
    login_dialog_title,
    login_error_wrong,
    login_input_label,
    login_prompt,
    main_error_llm_provider,
    main_info_check_config,
    main_llm_label,
    main_model_label,
    r00_title,
    r01_title,
    r02_title,
    r99_title,
)


def init_logging() -> None:
    """Initialize and and configure the logging."""
    logging.addLevelName(logging.DEBUG, "D")
    logging.addLevelName(logging.INFO, "I")
    logging.addLevelName(logging.WARNING, "W")
    logging.addLevelName(logging.ERROR, "E")
    logging.addLevelName(logging.CRITICAL, "C")
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("tornado").setLevel(logging.WARNING)
    logging.getLogger("google_genai").setLevel(logging.WARNING)


# def init_sentry() -> None:
#     """Initialize Sentry exception tracking/alerting."""
#     sentry_sdk.init(
#         dsn=st.secrets["sentry_dsn"],
#         environment="entorb.net",
#         send_default_pii=True,
#         traces_sample_rate=0.0,
#     )


# def init_matomo() -> None:
#     """Initialize Matomo access stats, via JavaScript snippet."""
#     import streamlit.components.v1 as components

#     components.html(
#         """
# <script>
# var _paq = window._paq = window._paq || [];
# _paq.push(['trackPageView']);
# _paq.push(['enableLinkTracking']);
# (function() {
#     var u="https://entorb.net/stats/matomo/";
#     _paq.push(['setTrackerUrl', u+'matomo.php']);
#     _paq.push(['setSiteId', '12']);
#     var d=document,g=d.createElement('script'),s=d.getElementsByTagName('script')[0];
#     g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
# })();
# </script>
#     """,
#         height=0,
#     )


@st.dialog(login_dialog_title, width="small", dismissible=False)
def show_login_dialog() -> None:
    """Display login dialog and handle authentication."""
    st.write(login_prompt)

    password = st.text_input(login_input_label, type="password")

    if st.button(login_btn_label, type="primary") or password:
        if password == st.secrets["login_password"]:
            st.session_state[SS_KEY_LOGGED_IN] = True

            # increase the login counter via web-stats script
            subprocess.run([WEBSTATS_SCRIPT, "mindchat"], check=False, shell=False)  # noqa: S603

            st.rerun()
        else:
            time.sleep(3)  # Mitigate brute-force attacks
            st.warning(login_error_wrong)


def show_login_page() -> None:
    """Show login page with dialog."""
    st.title(app_title)
    show_login_dialog()


def create_navigation() -> StreamlitPage:
    """Create Navigation Sidebar."""
    lst: list[StreamlitPage] = []
    lst.append(st.Page(page="reports/r00_info.py", title=r00_title))
    lst.append(st.Page(page="reports/r01_self.py", title=r01_title))
    lst.append(st.Page(page="reports/r02_chat.py", title=r02_title))
    lst.append(st.Page(page="reports/r99_logout.py", title=r99_title))
    page = st.navigation(pages=lst, position="sidebar", expanded=True)
    return page


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


def llm_select_in_sidebar() -> None:
    """Add select for LLM provider and model to sidebar."""
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


def version_date_in_sidebar() -> None:
    """Display last modification date of main.py."""
    deployment_date = dt.datetime.fromtimestamp(
        Path("src/main.py").stat().st_mtime, tz=dt.UTC
    ).astimezone(ZoneInfo("Europe/Berlin"))
    st.sidebar.markdown(f"Stand: {deployment_date.strftime('%d.%m.%y %H:%M')}")
