"""LLM module for handling language model interactions."""

from abc import ABC, abstractmethod
from functools import lru_cache

from config import LLM_PROVIDER


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def chat(self, system_message: str, messages: list[dict[str, str]]) -> str:
        """
        Generate a response from the LLM using conversation history.

        Args:
            system_message: The system instruction for the LLM
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The generated response

        """

    @abstractmethod
    def generate(self, system_message: str, prompt: str) -> str:
        """Single message chat."""


# Factory function to get LLM provider
@lru_cache(maxsize=1)
def get_llm_provider(provider: str = LLM_PROVIDER) -> LLMProvider:
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

    msg = f"Unknown LLM provider: {provider}"
    raise ValueError(msg)
