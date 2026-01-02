"""
Chat.

A chat interface where the user can interact with an AI psychotherapist
based on their self-disclosure.
"""

import streamlit as st

from llm import get_llm_provider

PREFIX = """
Du bist ein Psychotherapeut, der dieses Person berät:\n
"""


def main() -> None:  # noqa: D103
    st.title("Chat")

    self_disclosure = st.session_state.get("my-self-disclosure", "")

    if self_disclosure == "":
        st.write("Selbstauskunft ist leer")
        return

    st.markdown("""
- Hier kannst Du mit der KI chatten.
- Vorschläge für Fragen: Was sind meine Stärken? Worauf sollte ich achten?
""")

    instruction = PREFIX + self_disclosure

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
        with st.chat_message("assistant"), st.spinner("Denke nach..."):
            # Get LLM response using conversation history
            llm = get_llm_provider()
            response = llm.chat(instruction, st.session_state.chat_messages)

            st.write(response)

            # Add assistant response to chat history
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response}
            )

    # Add a button to clear chat history
    if st.button("Chat-Verlauf löschen"):
        st.session_state.chat_messages = []
        st.rerun()

    # # Optional: Show the instruction in an expander (collapsed by default)
    # with st.expander("System-Anweisung anzeigen"):
    #     st.code(instruction)


if __name__ == "__main__":
    main()
