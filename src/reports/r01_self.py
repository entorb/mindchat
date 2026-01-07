"""Selbstauskunft."""

import random

import streamlit as st

from config import (
    SD_TEMPLATE_PATH,
    SS_KEY_LLM_MODEL,
    SS_KEY_SD,
)
from llm import get_cached_llm_provider
from texts import (
    SPINNER_MESSAGES,
    r01_btn_feedback,
    r01_btn_save,
    r01_feedback_prompt,
    r01_header_feedback,
    r01_self_info,
    r01_success_saved,
    r01_textarea_label,
    r01_title,
)


@st.fragment
def text_editor() -> None:
    """Fragment for text editor to avoid full reruns."""
    # Initialize from template if not in session state
    if SS_KEY_SD not in st.session_state:
        self_disclosure = SD_TEMPLATE_PATH.read_text(encoding="utf-8")
        st.session_state[SS_KEY_SD] = self_disclosure

    text_content = st.text_area(
        label=r01_textarea_label,
        value=st.session_state[SS_KEY_SD],
        height=800,
    )

    # Save button to process and save content
    if st.button(r01_btn_save, type="primary") and text_content:
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
            st.success(r01_success_saved)


def main() -> None:  # noqa: D103
    st.title(r01_title)

    st.markdown(r01_self_info)

    # Text editor fragment
    text_editor()

    # Feedback section (separate from fragment to avoid re-rendering)
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
                    prompt=st.session_state[SS_KEY_SD],
                )
                st.markdown(response)


if __name__ == "__main__":
    main()
