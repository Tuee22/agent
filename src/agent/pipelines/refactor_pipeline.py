# src/agent/pipelines/refactor_pipeline.py
\"\"\"Refactor pipeline.\"\"\"

from __future__ import annotations

from ..config import AgentConfig
from ..core.conversation import Conversation
from ..core.pipeline_base import PipelineBase


class RefactorPipeline(PipelineBase):
    \"\"\"Runs specialised agent conversation for *refactor* tasks.\"\"\"

    def _conversation(self) -> Conversation:  # noqa: D401
        return Conversation(self._cfg)
