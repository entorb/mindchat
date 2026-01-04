"""
Chat.

A chat interface where the user can interact with an AI psychotherapist
based on their self-disclosure.
"""

import random
from datetime import UTC, datetime

import streamlit as st

from config import SPINNER_MESSAGES
from llm import get_llm_provider

PREFIX = """
Du bist ein Psychotherapeut, der dieses Person berät:\n
"""


def generate_markdown_export(system_message: str, messages: list) -> str:
    """Generate a markdown formatted string of the chat history."""
    markdown = "# Chat-Verlauf\n\n"
    markdown += "## 0. **KI Anweisung**\n\n"
    markdown += f"{system_message}\n\n"

    for i, message in enumerate(messages, 1):
        role = "Du" if message["role"] == "user" else "KI"
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
        label="Download Chatverlauf",
        data=markdown_content,
        file_name=filename,
        mime="text/markdown",
    )

    if cols[1].button("Chat-Verlauf löschen"):
        st.session_state.chat_messages = []
        st.rerun()


def main() -> None:  # noqa: D103
    st.title("Chat")
    st.markdown("""
- Hier kannst Du mit der KI chatten.
- Vorschläge für Fragen: Was sind meine Stärken? Worauf sollte ich achten?
""")

    if "my-self-disclosure" not in st.session_state:
        st.write("Selbstauskunft ist leer")
        return

    system_message = PREFIX + st.session_state["my-self-disclosure"]

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat messages from history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if user_input := st.chat_input("Stelle eine Frage..."):
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
