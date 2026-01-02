"""Logout."""

import streamlit as st


def main() -> None:  # noqa: D103
    st.title("Logout")
    for key in st.session_state:
        del st.session_state[key]

    st.write("Deine Daten wurden aus dem Arbeitsspeicher des Servers gelöscht.")


if __name__ == "__main__":
    main()
