"""Chat."""

import streamlit as st

PREFIX = """
Du bist ein Psychotherapeut, der dieses Person berät:\n
"""


def main() -> None:  # noqa: D103
    st.title("Chat")

    self_disclosure = st.session_state.get("my-self-disclosure", "")

    if self_disclosure == "":
        st.write("Selbstauskunft ist leer")
        return

    instruction = PREFIX + self_disclosure
    st.code(instruction)

    with st.chat_message("user"):
        st.write("user")
    with st.chat_message("assistant"):
        st.write("assistant")


if __name__ == "__main__":
    main()
