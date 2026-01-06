"""
Chat.
"""

import random
from datetime import UTC, datetime

import streamlit as st

from config import SD_KEY, SPINNER_MESSAGES
from llm import get_llm_provider
from texts import (
    r02_chat_info,
    r02_chat_input,
    r02_export_heading0,
    r02_export_title,
    r02_export_user_ai,
    r02_export_user_you,
    r02_hist_btn_del,
    r02_hist_btn_download,
    r02_missing_sd,
    r02_prompt_prefix,
    r02_title,
)


def generate_markdown_export(system_message: str, messages: list) -> str:
    """Generate a markdown formatted string of the chat history."""
    markdown = f"# {r02_export_title}\n\n"
    markdown += f"## 0. **{r02_export_heading0}**\n\n"
    markdown += f"{system_message}\n\n"

    for i, message in enumerate(messages, 1):
        role = r02_export_user_you if message["role"] == "user" else r02_export_user_ai
        markdown += f"---\n\n## {i}. **{role}**\n\n{message['content']}\n\n"

    return markdown


def show_history_buttons(system_message: str) -> None:
    """Show download and clear history buttons."""
    cols = st.columns(2)

    markdown_content = generate_markdown_export(
        system_message, st.session_state.chat_messages
    )

    filename = f"mindchat_{datetime.now(UTC).strftime('%Y%m%d_%H%M')}.md"

    cols[0].download_button(
        label=r02_hist_btn_download,
        data=markdown_content,
        file_name=filename,
        mime="text/markdown",
    )

    if cols[1].button(r02_hist_btn_del):
        st.session_state.chat_messages = []
        st.rerun()


def main() -> None:  # noqa: D103
    st.title(r02_title)
    st.markdown(r02_chat_info)

    if SD_KEY not in st.session_state:
        st.write(r02_missing_sd)
        return

    system_message = r02_prompt_prefix + st.session_state[SD_KEY]

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat messages from history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if user_input := st.chat_input(r02_chat_input):
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Generate assistant response
        with st.chat_message("assistant"), st.spinner(random.choice(SPINNER_MESSAGES)):  # noqa: S311
            # Call LLM
            llm = get_llm_provider()
            response = llm.chat(
                system_message=system_message, messages=st.session_state.chat_messages
            )

            # Display
            st.write(response)

            # Add assistant response to chat history
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response}
            )

    # Show history buttons only if there are chat messages
    if st.session_state.chat_messages:
        show_history_buttons(system_message)


if __name__ == "__main__":
    main()
