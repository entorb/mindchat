"""OpenAI LLM provider implementation."""

import streamlit as st
from openai import OpenAI

from llm import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI-based LLM provider."""

    def __init__(self, model: str = "gpt-5-nano") -> None:  # noqa: D107
        self.model = model
        self.client = OpenAI(api_key=st.secrets["openai_api_key"])

    def generate(self, instruction: str, prompt: str) -> str:
        """
        Generate a response using OpenAI.

        Args:
            instruction: The system instruction for the LLM
            prompt: The user prompt to respond to

        Returns:
            The generated response

        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error calling OpenAI: {e!s}"
