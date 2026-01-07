"""OpenAI LLM provider implementation."""

import logging

import streamlit as st
from openai import OpenAI

from llm import LLMProvider

logger = logging.getLogger(__name__)

MODELS = [
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-5",
]


class OpenAIProvider(LLMProvider):
    """OpenAI-based LLM provider."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(models=MODELS)
        self.client = OpenAI(api_key=st.secrets["openai_api_key"])

    def chat(  # noqa: D102
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        self.check_model(model)

        api_messages = [{"role": "system", "content": system_message}]
        api_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=model,
            messages=api_messages,  # type: ignore
        )
        return response.choices[0].message.content or ""
