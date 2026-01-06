"""OpenAI LLM provider implementation."""

import logging

import streamlit as st
from mistralai import Mistral

from config import LLM_MODEL
from llm import LLMProvider

logger = logging.getLogger(__name__)


class MistralProvider(LLMProvider):
    """Mistral-based LLM provider."""

    def __init__(self, model: str = LLM_MODEL) -> None:  # noqa: D107
        self.model = model
        self.client = Mistral(api_key=st.secrets["mistral_api_key"])

    def chat(self, system_message: str, messages: list[dict[str, str]]) -> str:
        """
        Generate a response using Mistral with conversation history.

        Args:
            system_message: The system instruction for the LLM
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The generated response

        """
        api_messages = [{"role": "system", "content": system_message}]
        api_messages.extend(messages)

        response = self.client.chat.complete(
            model=self.model,
            messages=api_messages,  # type: ignore
            stream=False,
        )
        return str(response.choices[0].message.content)

    def generate(self, system_message: str, prompt: str) -> str:
        """Single message chat."""
        return self.chat(
            system_message=system_message,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
