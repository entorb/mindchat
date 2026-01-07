"""Mistral LLM provider implementation."""

import logging
from typing import Any

import streamlit as st
from mistralai import Mistral

from llm import LLMProvider

logger = logging.getLogger(__name__)

MODELS = ["mistral-medium-latest"]


class MistralProvider(LLMProvider):
    """Mistral-based LLM provider."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(models=MODELS)
        try:
            if (
                not st.secrets.has_key("mistral_api_key")
                or st.secrets["mistral_api_key"] == ""
            ):
                st.error("Set your Mistral API key in .streamlit/secrets.toml")
                st.stop()
            # Create a new client instance for each session (no shared state)
            self.client = Mistral(api_key=st.secrets["mistral_api_key"])
        except KeyError:
            logger.exception("Mistral API key not found in secrets")
            msg = (
                "Mistral API key not configured. "
                "Please add 'mistral_api_key' to secrets."
            )
            raise ValueError(msg) from None
        except Exception:
            logger.exception("Failed to initialize Mistral client")
            raise

    def chat(
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        """
        Send a chat request with conversation history to Mistral.

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

            response = self.client.chat.complete(
                model=model,
                messages=api_messages,
                stream=False,
            )

            content = response.choices[0].message.content
            if not content:
                logger.warning("Empty response from Mistral")
                return ""

            return str(content)

        except Exception:
            logger.exception("Mistral API error")
            raise
