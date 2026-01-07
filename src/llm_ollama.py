"""Ollama LLM provider implementation."""

import logging

import ollama

from llm import LLMProvider

logger = logging.getLogger(__name__)

MODELS = [
    "mistral",
    "llama3.2:1b",
    "llama3.2:3b",
    "deepseek-r1:1.5b",
    "deepseek-r1:8b",
    "deepseek-r1:7b",
]


class OllamaProvider(LLMProvider):
    """Ollama-based LLM provider."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(models=MODELS)
        try:
            self.client = ollama.Client()
        except Exception:
            logger.exception("Failed to initialize Ollama client")
            msg = "Cannot connect to Ollama. Please ensure Ollama is running."
            raise ConnectionError(msg) from None

    def chat(
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        """
        Send a chat request with conversation history to Ollama.

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
            api_messages = [{"role": "system", "content": system_message}]
            api_messages.extend(messages)

            response = self.client.chat(
                model=model,
                messages=api_messages,
            )

            content = response.get("message", {}).get("content", "")
            if not content:
                logger.warning("Empty response from Ollama")
                return ""

            return str(content)

        except Exception:
            logger.exception("Ollama API error")
            raise
