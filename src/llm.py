"""LLM module for handling language model interactions."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, models: list[str]) -> None:  # noqa: D107
        self.models = models

    def check_model(self, model: str) -> None:  # noqa: D102
        if model not in self.models:
            msg = f"Model {model} not in available models: {self.models}"
            raise ValueError(msg)

    @abstractmethod
    def chat(
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        """
        Generate a response using the LLM with conversation history.

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
                {"role": "user", "content": prompt},
            ],
        )


# Factory function to get LLM provider
def get_llm_provider(provider: str) -> LLMProvider:
    """
    Get an LLM provider instance.

    This creates a NEW instance each time to ensure session isolation.
    Each Streamlit session should have its own provider instance.

    Args:
        provider: The provider name ('Ollama', 'OpenAI', 'Mistral', 'Google')

    Returns:
        LLM provider instance

    Raises:
        ValueError: If provider is unknown

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


def get_cached_llm_provider() -> LLMProvider:
    """
    Get LLM provider cached in session state for performance.

    Uses st.session_state to cache the provider instance per user session.
    The cached provider is explicitly cleared when LLM_PROVIDER changes in main.py.

    Returns:
        Cached LLM provider instance for current session

    """
    import streamlit as st  # noqa: PLC0415

    from config import (  # noqa: PLC0415
        SS_KEY_LLM_PROVIDER,
        SS_KEY_LLM_PROVIDER_INSTANCE,
    )

    # Create provider if not cached (cache cleared explicitly on provider change)
    if SS_KEY_LLM_PROVIDER_INSTANCE not in st.session_state:
        st.session_state[SS_KEY_LLM_PROVIDER_INSTANCE] = get_llm_provider(
            st.session_state[SS_KEY_LLM_PROVIDER]
        )

    return st.session_state[SS_KEY_LLM_PROVIDER_INSTANCE]
