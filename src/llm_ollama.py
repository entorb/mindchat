"""Ollama LLM provider implementation."""

import ollama

from llm import LLMProvider

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

    def chat(  # noqa: D102
        self, model: str, system_message: str, messages: list[dict[str, str]]
    ) -> str:
        self.check_model(model)

        api_messages = [{"role": "system", "content": system_message}]
        api_messages.extend(messages)

        response = ollama.chat(
            model=model,
            messages=api_messages,
        )
        return response["message"]["content"]
