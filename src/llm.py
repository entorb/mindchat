"""LLM module for handling language model interactions."""

from abc import ABC, abstractmethod


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


# Factory function to get LLM provider
def get_llm_provider(provider: str = "Ollama", **kwargs) -> LLMProvider:  # noqa: ANN003
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
    msg = f"Unknown LLM provider: {provider}"
    raise ValueError(msg)
