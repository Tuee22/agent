# src/agent/agents/coder.py
"""Agent that writes / refactors code."""

from __future__ import annotations

import re
from typing import Sequence

from ..config import AgentConfig
from ..core.agent_base import AgentBase, Message
from ..core.executor import Executor
from ..models.llm_base import LLMBase
from ..util.files import apply_diff
from ..util.prompts import CODER as SYSTEM


class CoderAgent(AgentBase):
    """LLM‑powered code writer."""

    _DIFF_RE = re.compile(r"```diff\n([\s\S]+?)```", re.MULTILINE)

    def __init__(self, llm: LLMBase, cfg: AgentConfig, executor: Executor) -> None:
        super().__init__("Coder")
        self._llm = llm
        self._root = cfg.project_path
        self._executor = executor

    # ------------------------------------------------------------------ #
    async def _apply_patches(self, text: str) -> str:
        """Find diff fences, write changes, return summary."""
        summaries: list[str] = []
        for diff in self._DIFF_RE.findall(text):
            # first line of diff contains --- a/file +++ b/file
            header = diff.splitlines()[0]
            _, filepath = header.split(" ", 1)
            path = self._root / filepath.strip()
            summary = apply_diff(path, diff)
            summaries.append(summary)
        return "\n".join(summaries)

    async def areply(self, history: Sequence[Message]) -> Message:
        prompt = SYSTEM + "\n\n" + "\n".join(f"{m.sender}: {m.content}" for m in history)
        content = await self._llm.acomplete(prompt)
        await self._apply_patches(content)
        return Message(self.name, content)
