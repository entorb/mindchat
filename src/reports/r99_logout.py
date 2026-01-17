"""Logout."""

import streamlit as st

from texts import r99_logout

# Clear all session state
keys_to_delete = list(st.session_state.keys())
for key in keys_to_delete:
    del st.session_state[key]

st.write(r99_logout)
