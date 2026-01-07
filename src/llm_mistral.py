"""OpenAI LLM provider implementation."""

import logging

import streamlit as st
from mistralai import Mistral

from llm import LLMProvider

logger = logging.getLogger(__name__)

MODELS = ["mistral-medium-latest"]


class MistralProvider(LLMProvider):
    """Mistral-based LLM provider."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(models=MODELS)
        self.client = Mistral(api_key=st.secrets["mistral_api_key"])

    def chat(  # noqa: D102
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        self.check_model(model)

        api_messages = [{"role": "system", "content": system_message}]
        api_messages.extend(messages)

        response = self.client.chat.complete(
            model=model,
            messages=api_messages,  # type: ignore
            stream=False,
        )
        return str(response.choices[0].message.content)
