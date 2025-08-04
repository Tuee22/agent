# src/agent/pipelines/test_pipeline.py
\"\"\"Test pipeline.\"\"\"

from __future__ import annotations

from ..config import AgentConfig
from ..core.conversation import Conversation
from ..core.pipeline_base import PipelineBase


class TestPipeline(PipelineBase):
    \"\"\"Runs specialised agent conversation for *test* tasks.\"\"\"

    def _conversation(self) -> Conversation:  # noqa: D401
        return Conversation(self._cfg)
