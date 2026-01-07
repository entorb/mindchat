"""
Chat.
"""

import random
from datetime import UTC, datetime

import streamlit as st

from config import (
    SS_KEY_CHAT_HISTORY,
    SS_KEY_LLM_MODEL,
    SS_KEY_SD,
)
from llm import get_cached_llm_provider
from models import ChatHistory
from texts import (
    SPINNER_MESSAGES,
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


def generate_markdown_export(system_message: str, history: ChatHistory) -> str:
    """Generate a markdown formatted string of the chat history."""
    markdown = f"# {r02_export_title}\n\n"
    markdown += f"## 0. **{r02_export_heading0}**\n\n"
    markdown += f"{system_message}\n\n"

    for i, message in enumerate(history.messages, 1):
        role = r02_export_user_you if message.role == "user" else r02_export_user_ai
        markdown += f"---\n\n## {i}. **{role}**\n\n{message.content}\n\n"

    return markdown


@st.fragment
def show_history_buttons(system_message: str, history: ChatHistory) -> None:
    """Show download and clear history buttons (wrapped in fragment)."""
    cols = st.columns(2)

    markdown_content = generate_markdown_export(system_message, history)

    filename = f"mindchat_{datetime.now(UTC).strftime('%Y%m%d_%H%M')}.md.txt"

    cols[0].download_button(
        label=r02_hist_btn_download,
        data=markdown_content,
        file_name=filename,
        mime="text/markdown",
    )

    if cols[1].button(r02_hist_btn_del):
        del st.session_state[SS_KEY_CHAT_HISTORY]
        # No st.rerun() needed - Streamlit auto-reruns on state change


def main() -> None:  # noqa: D103
    st.title(r02_title)
    st.markdown(r02_chat_info)

    if SS_KEY_SD not in st.session_state:
        st.write(r02_missing_sd)
        return

    system_message = r02_prompt_prefix + st.session_state[SS_KEY_SD]

    # Initialize chat history with Pydantic model
    # This persists across provider/model changes
    if SS_KEY_CHAT_HISTORY not in st.session_state:
        st.session_state[SS_KEY_CHAT_HISTORY] = ChatHistory(
            system_message=system_message
        )
    else:
        # Update system message if it changed
        st.session_state[SS_KEY_CHAT_HISTORY].system_message = system_message

    # Display chat messages from history
    for message in st.session_state[SS_KEY_CHAT_HISTORY].messages:
        with st.chat_message(message.role):
            st.write(message.content)

    # Chat input
    if user_input := st.chat_input(r02_chat_input):
        # Add user message to chat history
        st.session_state[SS_KEY_CHAT_HISTORY].add_message("user", user_input)

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Generate assistant response
        with st.chat_message("assistant"), st.spinner(random.choice(SPINNER_MESSAGES)):  # noqa: S311
            # Call LLM with proper message format
            llm = get_cached_llm_provider()
            response = llm.chat(
                model=st.session_state[SS_KEY_LLM_MODEL],
                system_message=system_message,
                messages=st.session_state[SS_KEY_CHAT_HISTORY].to_api_format(),
            )

            # Display
            st.write(response)

            # Add assistant response to chat history
            st.session_state[SS_KEY_CHAT_HISTORY].add_message("assistant", response)

    # Show history buttons only if there are chat messages
    if st.session_state[SS_KEY_CHAT_HISTORY].messages:
        show_history_buttons(system_message, st.session_state[SS_KEY_CHAT_HISTORY])


if __name__ == "__main__":
    main()
