# src/agent/core/pipeline_base.py
"""Abstract pipeline (selects a :class:`Conversation` and defines stop rules)."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod

from ..config import AgentConfig
from ..core.conversation import Conversation


class PipelineBase(ABC):
    """Common pipeline behaviour."""

    def __init__(self, cfg: AgentConfig) -> None:
        self._cfg = cfg

    async def arun(self, prompt: str) -> None:
        """Run the pipeline asynchronously."""
        convo = self._conversation()
        await convo.arun(prompt)

    @abstractmethod
    def _conversation(self) -> Conversation: ...
