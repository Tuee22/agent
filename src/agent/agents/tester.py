# src/agent/agents/tester.py
"""Agent that runs pytest and reports exact failures."""

from __future__ import annotations

from typing import Sequence

from ..config import AgentConfig
from ..core.agent_base import AgentBase, Message
from ..core.executor import Executor
from ..models.llm_base import LLMBase
from ..util.prompts import TESTER as SYSTEM


class TesterAgent(AgentBase):
    """Runs `pytest -q` and returns results verbatim."""

    def __init__(self, llm: LLMBase, cfg: AgentConfig, executor: Executor) -> None:
        super().__init__("Tester")
        self._llm = llm  # not used but keeps uniform API
        self._executor = executor

    async def areply(self, history: Sequence[Message]) -> Message:  # noqa: D401
        rc, out, err = await self._executor.arun(["pytest", "-q"])
        report = f"exit={rc}\nstdout:\n{out}\nstderr:\n{err}"
        return Message(self.name, report)
