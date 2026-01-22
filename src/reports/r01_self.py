"""Selbstauskunft."""

import random
from io import StringIO

import streamlit as st

from config import (
    PATH_PAGE_CHAT,
    PATH_SD_TEMPLATE,
    SS_KEY_LLM_MODEL,
    SS_KEY_SD,
)
from helper import current_date_time_for_filenames
from llm import get_cached_llm_provider
from texts import (
    SPINNER_MESSAGES,
    r01_btn_chat,
    r01_btn_download,
    r01_btn_feedback,
    r01_btn_upload,
    r01_feedback_prompt,
    r01_header_feedback,
    r01_self_info,
    r01_textarea_label,
)

KEY_TEXTAREA = "text_area_temp"


def cleanup_and_save_content() -> None:
    """Process and save content automatically on change."""
    text_content = st.session_state[KEY_TEXTAREA]

    # perform some cleanup
    text_content = text_content.strip()
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


def text_editor() -> None:
    """Text editor, that saves automatically."""
    # Initialize from template if not in session state
    if SS_KEY_SD not in st.session_state:
        self_disclosure = PATH_SD_TEMPLATE.read_text(encoding="utf-8")
        st.session_state[SS_KEY_SD] = self_disclosure

    # If textarea key doesn't exist, initialize it with SS_KEY_SD value
    if KEY_TEXTAREA not in st.session_state:
        st.session_state[KEY_TEXTAREA] = st.session_state[SS_KEY_SD]

    st.text_area(
        label=r01_textarea_label,
        height=800,
        key=KEY_TEXTAREA,
        on_change=cleanup_and_save_content,
    )


def file_upload() -> None:
    """File upload widget and processing."""
    uploaded_file = st.file_uploader(
        r01_btn_upload,
        type="txt",
        accept_multiple_files=False,
    )
    if uploaded_file and not st.session_state.get("file_processed", False):
        bytes_data = uploaded_file.getvalue()
        string_io = StringIO(bytes_data.decode("utf-8"))
        string_data = string_io.read()
        st.session_state[SS_KEY_SD] = string_data
        # Clear the text_area_temp key to force recreation with new value
        if KEY_TEXTAREA in st.session_state:
            del st.session_state[KEY_TEXTAREA]
        # Mark file as processed to prevent loop
        st.session_state["file_processed"] = True
        st.success("Hochgeladen")
        st.rerun()
    elif not uploaded_file:
        # Reset the processed flag when uploader is cleared
        st.session_state["file_processed"] = False


def main() -> None:  # noqa: D103
    st.markdown(r01_self_info)

    text_editor()

    file_upload()

    # Download and Feedback section (separate from fragment to avoid re-rendering)
    if SS_KEY_SD in st.session_state:
        cols = st.columns(3)

        # Download
        filename = f"mindchat_self_{current_date_time_for_filenames()}.md.txt"
        _btn_download = cols[0].download_button(
            label=r01_btn_download,
            data=st.session_state[SS_KEY_SD],
            file_name=filename,
            mime="text/markdown",
        )

        # Chat
        btn_chat = cols[1].button(r01_btn_chat, type="primary")
        if btn_chat:
            st.switch_page(PATH_PAGE_CHAT)

        btn_feedback = cols[2].button(r01_btn_feedback)
        if btn_feedback:
            st.header(r01_header_feedback)
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
