"""OpenAI LLM provider implementation."""

import logging

import streamlit as st
from openai import OpenAI

from config import LLM_MODEL
from llm import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI-based LLM provider."""

    def __init__(self, model: str = LLM_MODEL) -> None:  # noqa: D107
        self.model = model
        self.client = OpenAI(api_key=st.secrets["openai_api_key"])

    def generate(self, system_message: str, prompt: str) -> str:
        """
        Generate a response using OpenAI.

        Args:
            system_message: The system instruction for the LLM
            prompt: The user prompt to respond to

        Returns:
            The generated response

        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content or ""

    def chat(self, system_message: str, messages: list[dict[str, str]]) -> str:
        """
        Generate a response using OpenAI with conversation history.

        Args:
            system_message: The system instruction for the LLM
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The generated response

        """
        api_messages = [{"role": "system", "content": system_message}]
        api_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,  # type: ignore
        )
        return response.choices[0].message.content or ""
