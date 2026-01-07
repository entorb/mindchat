"""Google Gemini LLM provider implementation."""

import logging

import streamlit as st
from google import genai
from google.genai import types as genai_types

from llm import LLMProvider

logger = logging.getLogger(__name__)

MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]


class GoogleProvider(LLMProvider):
    """Google Gemini-based LLM provider."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(models=MODELS)
        try:
            # Create a new client instance for each session (no shared state)
            self.client = genai.Client(api_key=st.secrets["google_api_key"])
        except KeyError:
            logger.exception("Google API key not found in secrets")
            msg = "Google API key not configured. Please add 'google_api_key' to secrets."
            raise ValueError(msg) from None
        except Exception:
            logger.exception("Failed to initialize Google client")
            raise

    def chat(
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        """
        Send a chat request with conversation history to the Gemini API.

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
            # Convert messages to Gemini format
            # Gemini expects alternating user/model messages
            # Filter out system messages as they're handled separately
            gemini_messages = []
            for msg in messages[:-1]:  # All except the last message
                if msg["role"] == "system":
                    continue  # Skip system messages in history
                gemini_messages.append(
                    {
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [{"text": msg["content"]}],
                    }
                )

            # Create chat with history
            chat = self.client.chats.create(
                model=model,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_message
                ),
                history=gemini_messages,  # type: ignore[arg-type]
            )

            # Send the latest user message
            last_message = messages[-1]["content"]
            response = chat.send_message(last_message)

            if not response or not response.text:
                logger.warning("Empty response from Google Gemini")
                return ""

            return str(response.text)

        except Exception:
            logger.exception("Google Gemini API error")
            raise

    def generate(self, model: str, system_message: str, prompt: str) -> str:
        """
        Generate a single response without conversation history.

        Args:
            model: The model name to use
            system_message: System instruction for the model
            prompt: The user prompt

        Returns:
            The model's response text

        Raises:
            ValueError: If model is not supported
            Exception: If the API call fails

        """
        self.check_model(model)

        try:
            response = self.client.models.generate_content(
                model=model,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_message
                ),
                contents=prompt,
            )

            if not response or not response.text:
                logger.warning("Empty response from Google Gemini")
                return ""

            return str(response.text)

        except Exception:
            logger.exception("Google Gemini API error")
            raise
