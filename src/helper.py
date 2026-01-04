"""Helper Functions."""

import logging
import time

import sentry_sdk
import streamlit as st
from streamlit.navigation.page import StreamlitPage


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


def init_sentry() -> None:
    """Initialize Sentry exception tracking/alerting."""
    sentry_sdk.init(
        dsn=st.secrets["sentry_dsn"],
        environment="entorb.net",
        send_default_pii=True,
        traces_sample_rate=0.0,
    )


def init_matomo() -> None:
    """Initialize Matomo access stats, via JavaScript snippet."""
    import streamlit.components.v1 as components  # noqa: PLC0415

    components.html(
        """
<script>
var _paq = window._paq = window._paq || [];
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
    var u="https://entorb.net/stats/matomo/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '12']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
})();
</script>
    """,
        height=0,
    )


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


def create_navigation() -> StreamlitPage:
    """Create Navigation Sidebar."""
    lst: list[StreamlitPage] = []
    lst.append(st.Page(page="reports/r00_info.py", title="Info"))
    lst.append(st.Page(page="reports/r01_self.py", title="Selbstauskunft"))
    lst.append(st.Page(page="reports/r02_chat.py", title="Chat"))
    lst.append(st.Page(page="reports/r99_logout.py", title="Logout"))
    page = st.navigation(pages=lst, position="sidebar", expanded=True)
    page.run()
    return page
