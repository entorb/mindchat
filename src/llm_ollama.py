"""Ollama LLM provider implementation."""

import ollama

from llm import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama-based LLM provider."""

    def __init__(self, model: str = "llama3.2") -> None:  # noqa: D107
        self.model = model

    def generate(self, instruction: str, prompt: str) -> str:
        """
        Generate a response using Ollama.

        Args:
            instruction: The system instruction for the LLM
            prompt: The user prompt to respond to

        Returns:
            The generated response

        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        except Exception as e:  # noqa: BLE001
            # TODO: logger
            return f"Error calling Ollama: {e!s}"

    def chat(self, system_message: str, messages: list[dict[str, str]]) -> str:
        """
        Generate a response using Ollama with conversation history.

        Args:
            system_message: The system instruction for the LLM
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            The generated response

        """
        try:
            api_messages = [{"role": "system", "content": system_message}]
            api_messages.extend(messages)

            response = ollama.chat(
                model=self.model,
                messages=api_messages,
            )
            return response["message"]["content"]
        except Exception as e:  # noqa: BLE001
            # TOOD: logger
            return f"Error calling Ollama: {e!s}"
