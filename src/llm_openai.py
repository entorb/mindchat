"""OpenAI LLM provider implementation."""

import logging
from typing import Any

import streamlit as st
from openai import OpenAI

from llm import LLMProvider

LOGGER = logging.getLogger(__name__)

MODELS = [
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-5",
]


class OpenAIProvider(LLMProvider):
    """OpenAI-based LLM provider."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(models=MODELS)
        try:
            if (
                not st.secrets.has_key("openai_api_key")
                or st.secrets["openai_api_key"] == ""
            ):
                st.error("Set your OpenAI API key in .streamlit/secrets.toml")
                st.stop()
            # Create a new client instance for each session (no shared state)
            self.client = OpenAI(api_key=st.secrets["openai_api_key"])
        except KeyError:
            LOGGER.exception("OpenAI API key not found in secrets")
            msg = (
                "OpenAI API key not configured. Please add 'openai_api_key' to secrets."
            )
            raise ValueError(msg) from None
        except Exception:
            LOGGER.exception("Failed to initialize OpenAI client")
            raise

    def chat(
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        """
        Send a chat request with conversation history to OpenAI.

        Args:
            model: The model name to use
            system_message: System instruction for the model
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The model's response text

        Raises:
            ValueError: If model is not supported
            Exception: If the API call fails

        """
        self.check_model(model)

        try:
            api_messages: list[dict[str, Any]] = [
                {"role": "system", "content": system_message}
            ]
            api_messages.extend(messages)

            response = self.client.chat.completions.create(
                model=model,
                messages=api_messages,
            )

            content = response.choices[0].message.content
            if not content:
                LOGGER.warning("Empty response from OpenAI")
            else:
                return content

        except Exception:
            LOGGER.exception("OpenAI API error")
            raise
