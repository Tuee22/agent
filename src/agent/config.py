# src/agent/config.py
"""Typed user configuration objects."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Literal, Mapping, Tuple

from pydantic import BaseModel, Field, validator

ProviderName = Literal["openai", "anthropic"]
ModelDescriptor = Tuple[ProviderName, str]


class VectorStoreConfig(BaseModel):
    """Settings for Chroma vector DB."""

    persist: bool = Field(False, description="Persist index on disk?")
    persist_path: Path | None = Field(
        None, description="Directory for the persistent index"
    )

    @validator("persist_path", always=True)
    def _path_required(cls, v: Path | None, values: Mapping[str, Any]) -> Path | None:
        if values.get("persist") and v is None:
            raise ValueError("`persist_path` must be set when `persist=True`.")
        return v


class ExecutionConfig(BaseModel):
    """Sandbox / runtime settings for executing generated code."""

    use_docker: bool = Field(True, description="Run commands inside Docker.")
    image: str = Field("python:3.12-slim", description="Docker image.")
    timeout: int = Field(60, description="Seconds allowed per command.")


class AgentConfig(BaseModel):
    """Master configuration consumed by :class:`agent.core.system.AgentSystem`."""

    project_path: Path = Field(..., description="Folder that will be modified in‑place.")
    model_providers: Dict[str, ModelDescriptor] = Field(
        ...,
        description='Mapping agent_role → (provider, model). '
        'Example: {"coder": ("openai", "gpt-4o")}',
    )
    provider_configs: Dict[ProviderName, Dict[str, Any]] = Field(
        ..., description="API keys & default parameters per provider."
    )
    embedding_provider: ModelDescriptor = Field(
        ..., description="(provider, model) used for semantic search."
    )
    embedding_config: Dict[str, Any] = Field(
        default_factory=dict, description="API key & kwargs for embeddings."
    )
    vector_store: VectorStoreConfig = Field(
        default_factory=VectorStoreConfig, description="ChromaDB settings."
    )
    execution: ExecutionConfig = Field(
        default_factory=ExecutionConfig, description="Code‑execution sandbox."
    )
    max_iterations: int = Field(
        12, description="Safety valve: pipeline stops after this many cycles."
    )

    class Config:
        frozen = True
        validate_assignment = True
