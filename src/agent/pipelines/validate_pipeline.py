# src/agent/pipelines/validate_pipeline.py
\"\"\"Validate pipeline.\"\"\"

from __future__ import annotations

from ..config import AgentConfig
from ..core.conversation import Conversation
from ..core.pipeline_base import PipelineBase


class ValidatePipeline(PipelineBase):
    \"\"\"Runs specialised agent conversation for *validate* tasks.\"\"\"

    def _conversation(self) -> Conversation:  # noqa: D401
        return Conversation(self._cfg)
