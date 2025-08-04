# src/agent/agents/reviewer.py
"""Agent that lints code and asks for fixes."""

from __future__ import annotations

from typing import Sequence

from ..config import AgentConfig
from ..core.agent_base import AgentBase, Message
from ..core.executor import Executor
from ..models.llm_base import LLMBase
from ..util.prompts import REVIEWER as SYSTEM


class ReviewerAgent(AgentBase):
    """Runs flake8, summarises violations."""

    def __init__(self, llm: LLMBase, cfg: AgentConfig, executor: Executor) -> None:
        super().__init__("Reviewer")
        self._executor = executor
        self._llm = llm  # optional follow‑up completions

    async def areply(self, history: Sequence[Message]) -> Message:
        rc, out, err = await self._executor.arun(["flake8", "."])
        body = "No issues ✅" if rc == 0 else f"flake8 exit={rc}\n{out or err}"
        return Message(self.name, body)
