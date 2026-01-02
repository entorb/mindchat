"""Logout."""

import streamlit as st


def main() -> None:  # noqa: D103
    st.title("Logout")

    # Clear all session state
    keys_to_delete = list(st.session_state.keys())
    for key in keys_to_delete:
        del st.session_state[key]

    st.write(
        "Abgemeldet: Deine Daten wurden aus dem Arbeitsspeicher des Servers gelöscht"
    )


if __name__ == "__main__":
    main()
