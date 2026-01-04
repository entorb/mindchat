"""Logout."""

import streamlit as st

from text import r99_logout


def main() -> None:  # noqa: D103
    st.title("Logout")

    # Clear all session state
    keys_to_delete = list(st.session_state.keys())
    for key in keys_to_delete:
        del st.session_state[key]

    st.write(r99_logout)


if __name__ == "__main__":
    main()
