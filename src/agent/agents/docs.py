# src/agent/agents/docs.py
"""Agent that generates documentation updates."""

from __future__ import annotations

from typing import Sequence

from ..config import AgentConfig
from ..core.agent_base import AgentBase, Message
from ..models.llm_base import LLMBase
from ..util.prompts import DOCS as SYSTEM


class DocsAgent(AgentBase):
    """Writes or updates Google‑style docstrings."""

    def __init__(self, llm: LLMBase, cfg: AgentConfig) -> None:
        super().__init__("DocWriter")
        self._llm = llm

    async def areply(self, history: Sequence[Message]) -> Message:
        prompt = SYSTEM + "\n\nConversation:\n" + "\n".join(f"{m.sender}: {m.content}" for m in history)
        content = await self._llm.acomplete(prompt)
        return Message(self.name, content)
