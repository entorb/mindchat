"""Selbstauskunft."""

import random

import streamlit as st

from config import (
    SD_TEMPLATE_PATH,
    SPINNER_MESSAGES,
    SS_KEY_LLM_MODEL,
    SS_KEY_SD,
)
from llm import get_cached_llm_provider
from texts import (
    r01_btn_feedback,
    r01_btn_save,
    r01_feedback_prompt,
    r01_header_feedback,
    r01_self_info,
    r01_textarea_label,
    r01_title,
)


def main() -> None:  # noqa: D103
    st.title(r01_title)

    st.markdown(r01_self_info)

    if SS_KEY_SD in st.session_state:
        self_disclosure = st.session_state[SS_KEY_SD]
    else:
        # initialize from template
        self_disclosure = SD_TEMPLATE_PATH.read_text(encoding="utf-8")

    text_content = st.text_area(
        label=r01_textarea_label,
        value=self_disclosure,
        height=800,  # fallback height
    )
    # 2nd save button to prevent data loss
    btn_save = st.button(r01_btn_save, type="primary")

    if btn_save and text_content:
        text_content = text_content.strip()
        # loop over all lines
        lines = text_content.split("\n")
        processed_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("##") and "(" in stripped:
                stripped = stripped.split("(")[0].strip()
            processed_lines.append(stripped)
        text_content = "\n".join(processed_lines)

        if text_content != "":
            st.session_state[SS_KEY_SD] = text_content

    if SS_KEY_SD in st.session_state and st.session_state[SS_KEY_SD] != "":
        st.header(r01_header_feedback)
        btn_feedback = st.button(r01_btn_feedback)

        if btn_feedback:
            with st.spinner(random.choice(SPINNER_MESSAGES)):  # noqa: S311
                instruction = r01_feedback_prompt
                llm = get_cached_llm_provider()
                response = llm.generate(
                    model=st.session_state[SS_KEY_LLM_MODEL],
                    system_message=instruction,
                    prompt=text_content,
                )
                st.markdown(response)


if __name__ == "__main__":
    main()
