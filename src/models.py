"""Pydantic models for data structures."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(..., pattern="^(system|user|assistant|model)$")
    content: str = Field(..., min_length=1)

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary format for API calls."""
        return {"role": self.role, "content": self.content}


class ChatHistory(BaseModel):
    """Chat history container with validation."""

    messages: list[ChatMessage] = Field(default_factory=list)
    system_message: str = ""

    def add_message(self, role: str, content: str) -> None:
        """Add a message to history."""
        self.messages.append(ChatMessage(role=role, content=content))

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    def to_api_format_with_system(self) -> list[dict[str, str]]:
        """
        Convert to API format including system message.

        Returns:
            List of message dicts with system message prepended

        """
        messages = [msg.to_dict() for msg in self.messages]
        if self.system_message:
            messages.insert(0, {"role": "system", "content": self.system_message})
        return messages

    def to_api_format(self) -> list[dict[str, str]]:
        """
        Convert to API format (list of dicts) without system message.

        Returns:
            List of message dicts suitable for API calls

        """
        return [msg.to_dict() for msg in self.messages]

    def get_user_assistant_messages(self) -> list[dict[str, str]]:
        """Get only user and assistant messages (no system)."""
        return [
            msg.to_dict() for msg in self.messages if msg.role in ("user", "assistant")
        ]

    def __len__(self) -> int:
        """Return number of messages."""
        return len(self.messages)
