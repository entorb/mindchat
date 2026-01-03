"""Selbstauskunft."""

from pathlib import Path

import streamlit as st

from llm import get_llm_provider


def main() -> None:  # noqa: D103
    st.title("Selbstauskunft")

    st.markdown("""
- Fülle diese Selbstauskunft aus, damit Du mit der KI über Dich chatten kannst
- Zeilen mit '##' sind Überschriften, lösche gerne irrelevante oder füge weitere ein
- Wichtig: "Speichen" um die Daten zu übernehmen
- Tipp: Falls Du diese App nochmal verwenden willst, kopiere und speichere den Text hinterher auf dein Gerät, da beim Abmelden alle Deinen Daten vom Server gelöscht werden.""")  # noqa: E501

    if "my-self-disclosure" in st.session_state:
        self_disclosure = st.session_state["my-self-disclosure"]
    else:
        # initialize from template
        self_disclosure = Path("src/prompts/self-disclosure-template.md").read_text()

    text_content = st.text_area(
        label="Selbstauskunft",
        value=self_disclosure,
        height=800,  # fallback height
        placeholder="Enter your text here...",
    )
    # 2nd save button to prevent data loss
    btn_save = st.button("Speichern", key="btn_save2", type="primary")

    if btn_save and text_content:
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

        if text_content != "":
            st.session_state["my-self-disclosure"] = text_content

    if (
        "my-self-disclosure" in st.session_state
        and st.session_state["my-self-disclosure"] != ""
    ):
        st.header("Feedback")
        btn_feedback = st.button("KI Feedback einholen")

        if btn_feedback:
            instruction = Path("src/prompts/self-disclosure-feedback.md").read_text()
            llm = get_llm_provider()
            response = llm.generate(instruction, prompt=text_content)
            st.markdown(response)


if __name__ == "__main__":
    main()
