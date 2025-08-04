# src/agent/core/system.py
"""Facade combining config → pipeline → conversation."""

from __future__ import annotations

import asyncio
from typing import Literal, Mapping, Type

from ..config import AgentConfig
from ..pipelines.refactor_pipeline import RefactorPipeline
from ..pipelines.docs_pipeline import DocsPipeline
from ..pipelines.test_pipeline import TestPipeline
from ..pipelines.validate_pipeline import ValidatePipeline
from ..core.pipeline_base import PipelineBase

PipelineName = Literal["refactor", "docs", "test", "validate"]

_PIPELINES: Mapping[PipelineName, Type[PipelineBase]] = {
    "refactor": RefactorPipeline,
    "docs": DocsPipeline,
    "test": TestPipeline,
    "validate": ValidatePipeline,
}


class AgentSystem:
    """Public API: run a chosen pipeline."""

    def __init__(self, cfg: AgentConfig) -> None:
        self._cfg = cfg

    # ------------------------------------------------------------------ #
    def run_pipeline(self, pipeline: PipelineName, prompt: str) -> None:
        """Execute *pipeline* synchronously."""
        cls = _PIPELINES[pipeline]
        asyncio.run(cls(self._cfg).arun(prompt))
