"""Selbstauskunft."""

import streamlit as st

from config import PATH_PAGE_SELF
from texts import r00_btn_self, r00_info

st.markdown(r00_info)

btn_chat = st.button(r00_btn_self, type="primary")
if btn_chat:
    st.switch_page(PATH_PAGE_SELF)
