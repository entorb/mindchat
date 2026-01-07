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
        self.client = genai.Client(api_key=st.secrets["google_api_key"])

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

        """
        self.check_model(model)
        # Convert messages to Gemini format
        # Gemini expects alternating user/model messages
        gemini_messages = [
            {
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}],
            }
            for msg in messages[:-1]  # All except the last message
        ]

        # Create chat with history
        chat = self.client.chats.create(
            model=model,
            config=genai_types.GenerateContentConfig(system_instruction=system_message),
            history=gemini_messages,  # type: ignore[arg-type]
        )

        # Send the latest user message
        last_message = messages[-1]["content"]
        response = chat.send_message(last_message)

        return str(response.text) if response else ""

    def generate(self, model: str, system_message: str, prompt: str) -> str:
        """
        Generate a single response without conversation history.

        Args:
            model: The model name to use
            system_message: System instruction for the model
            prompt: The user prompt

        Returns:
            The model's response text

        """
        self.check_model(model)
        response = self.client.models.generate_content(
            model=model,
            config=genai_types.GenerateContentConfig(system_instruction=system_message),
            contents=prompt,
        )
        return str(response.text) if response else ""
