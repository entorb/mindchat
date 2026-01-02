"""Selbstauskunft."""

from pathlib import Path

import streamlit as st

from llm import get_llm_provider


def main() -> None:  # noqa: D103
    st.title("Selbstauskunft")

    st.markdown("""Fülle diese Selbstauskunft aus.""")

    if "my-self-disclosure" in st.session_state:
        self_disclosure = st.session_state["my-self-disclosure"]
    else:
        # initialize from template
        self_disclosure = Path("src/prompts/self-disclosure-template.md").read_text()

    btn_save1 = st.button("Speichern", key="btn_save1", type="primary")
    text_content = st.text_area(
        label="",
        value=self_disclosure,
        height=400,  # fallback height
        placeholder="Enter your text here...",
    )
    # 2nd save button to prevent data loss
    btn_save2 = st.button("Speichern", key="btn_save2", type="primary")

    if text_content:
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

        if btn_save1 or btn_save2:
            st.session_state["my-self-disclosure"] = text_content

        st.header("Feedback")
        btn_feedback = st.button("KI Feedback einholen")

        if btn_feedback:
            instruction = Path("src/prompts/self-disclosure-feedback.md").read_text()
            llm = get_llm_provider()
            response = llm.generate(instruction, prompt=text_content)
            st.markdown(response)


if __name__ == "__main__":
    main()
