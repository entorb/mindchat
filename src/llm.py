"""LLM module for handling language model interactions."""

from abc import ABC, abstractmethod
from functools import lru_cache


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, models: list[str]) -> None:  # noqa: D107
        self.models = models

    def check_model(self, model: str) -> None:  # noqa: D102
        assert model in self.models

    @abstractmethod
    def chat(
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        """
        Generate a response using Ollama with conversation history.

        Args:
            model: the LLM model to use, must be one of self.models
            system_message: The system instruction for the LLM
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The generated response

        """

    def generate(self, model: str, system_message: str, prompt: str) -> str:
        """Single message chat."""
        return self.chat(
            model=model,
            system_message=system_message,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )


# Factory function to get LLM provider
@lru_cache(maxsize=1)
def get_llm_provider(provider: str) -> LLMProvider:
    """
    Get an LLM provider instance.

    Args:
        provider: The provider name ('Ollama' for now)
        **kwargs: Additional arguments for the provider

    Returns:
        LLM provider instance

    """
    if provider == "Ollama":
        from llm_ollama import OllamaProvider  # noqa: PLC0415

        return OllamaProvider()

    if provider == "OpenAI":
        from llm_openai import OpenAIProvider  # noqa: PLC0415

        return OpenAIProvider()

    if provider == "Mistral":
        from llm_mistral import MistralProvider  # noqa: PLC0415

        return MistralProvider()

    if provider == "Google":
        from llm_google import GoogleProvider  # noqa: PLC0415

        return GoogleProvider()

    msg = f"Unknown LLM provider: {provider}"
    raise ValueError(msg)
