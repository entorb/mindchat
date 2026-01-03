"""LLM module for handling language model interactions."""

from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path

# TODO: helper ENV
if Path("/var/www/virtual/entorb/html").exists():
    DEFAULT_LLM_PROVIDER = "OpenAI"
else:
    DEFAULT_LLM_PROVIDER = "Ollama"


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, instruction: str, prompt: str) -> str:
        """
        Generate a response from the LLM.

        Args:
            instruction: The system instruction for the LLM
            prompt: The user prompt to respond to

        Returns:
            The generated response

        """

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


# Factory function to get LLM provider
@lru_cache(maxsize=1)
def get_llm_provider(provider: str = DEFAULT_LLM_PROVIDER, **kwargs) -> LLMProvider:  # noqa: ANN003
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

        return OllamaProvider(**kwargs)
    if provider == "OpenAI":
        from llm_openai import OpenAIProvider  # noqa: PLC0415

        return OpenAIProvider(**kwargs)
    msg = f"Unknown LLM provider: {provider}"
    raise ValueError(msg)
