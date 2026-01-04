"""Ollama LLM provider implementation."""

import ollama

from config import LLM_MODEL
from llm import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama-based LLM provider."""

    def __init__(self, model: str = LLM_MODEL) -> None:  # noqa: D107
        self.model = model

    def generate(self, system_message: str, prompt: str) -> str:
        """
        Generate a response using Ollama.

        Args:
            system_message: The system instruction for the LLM
            prompt: The user prompt to respond to

        Returns:
            The generated response

        """
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]

    def chat(self, system_message: str, messages: list[dict[str, str]]) -> str:
        """
        Generate a response using Ollama with conversation history.

        Args:
            system_message: The system instruction for the LLM
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The generated response

        """
        api_messages = [{"role": "system", "content": system_message}]
        api_messages.extend(messages)

        response = ollama.chat(
            model=self.model,
            messages=api_messages,
        )
        return response["message"]["content"]
