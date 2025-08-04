# src/agent/core/conversation.py
"""AutoGen GroupChat wiring."""

from __future__ import annotations

import asyncio
from typing import List

from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent  # type: ignore

from ..config import AgentConfig
from ..core.agent_base import Message
from ..core.executor import Executor
from ..models.llm_base import OpenAIModel
from ..agents.coder import CoderAgent
from ..agents.tester import TesterAgent
from ..agents.reviewer import ReviewerAgent
from ..agents.docs import DocsAgent


class Conversation:
    """Spin up specialised agents inside an AutoGen GroupChat."""

    def __init__(self, cfg: AgentConfig) -> None:
        self._cfg = cfg
        exec_ = Executor(cfg.execution, cfg.project_path)

        # Instantiate LLM backends
        pconf = cfg.provider_configs["openai"]
        coder_llm = OpenAIModel(cfg.model_providers["coder"][1], **pconf)
        tester_llm = OpenAIModel(cfg.model_providers["tester"][1], **pconf)
        reviewer_llm = OpenAIModel(cfg.model_providers["reviewer"][1], **pconf)

        # Concrete agents
        coder = CoderAgent(coder_llm, cfg, exec_)
        tester = TesterAgent(tester_llm, cfg, exec_)
        reviewer = ReviewerAgent(reviewer_llm, cfg, exec_)
        docs = DocsAgent(reviewer_llm, cfg)  # reuse LLM

        # Wrap in AssistantAgent so AutoGen can drive them ----------------
        def _wrap(a):
            async def _run(agent, messages, sender):  # noqa: ANN001
                msg_objs = [Message(m["role"], m["content"]) for m in messages]
                reply = await a.areply(msg_objs)
                return reply.content

            return AssistantAgent(name=a.name, llm_config={"callback": _run})

        assistants: List[AssistantAgent] = list(map(_wrap, (coder, tester, reviewer, docs)))

        self._group_manager = GroupChatManager(
            groupchat=GroupChat(assistants, messages=[]),
            llm_config={"timeout": cfg.execution.timeout},
        )
        self._user = UserProxyAgent("User", code_execution_config=False, llm_config=False)

    # ------------------------------------------------------------------ #
    async def arun(self, prompt: str) -> None:
        """Start chatting until ``GroupChatManager`` decides to stop."""
        await self._user.a_send(recipient=self._group_manager, message=prompt)
        while not self._group_manager.is_finished():
            await asyncio.sleep(0.5)
