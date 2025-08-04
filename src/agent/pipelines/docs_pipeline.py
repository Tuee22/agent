# src/agent/pipelines/docs_pipeline.py
\"\"\"Docs pipeline.\"\"\"

from __future__ import annotations

from ..config import AgentConfig
from ..core.conversation import Conversation
from ..core.pipeline_base import PipelineBase


class DocsPipeline(PipelineBase):
    \"\"\"Runs specialised agent conversation for *docs* tasks.\"\"\"

    def _conversation(self) -> Conversation:  # noqa: D401
        return Conversation(self._cfg)
