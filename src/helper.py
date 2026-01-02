"""Helper Functions."""

import sentry_sdk
import streamlit as st


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
