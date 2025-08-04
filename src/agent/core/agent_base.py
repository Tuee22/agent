# src/agent/core/agent_base.py
"""Abstract conversational agent wrapper."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence


class Message:
    """A chat message."""

    def __init__(self, sender: str, content: str) -> None:
        self.sender = sender
        self.content = content


class AgentBase(ABC):
    """Every concrete agent must be able to *reply*."""

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        """Display name (used in chat transcripts)."""
        return self._name

    @abstractmethod
    async def areply(self, history: Sequence[Message]) -> Message:
        """Produce next message given *history*."""
