from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, HttpUrl, SecretStr, field_validator


class Settings(BaseSettings):
    """Global application configuration."""

    openai_api_key: SecretStr | None = None
    openai_base_url: HttpUrl | None = None

    model_name: str = "gpt-4o-mini"
    embeddings_model_name: str = "gpt-embeddings-mini"

    project_root: Path = Path(".").resolve()
    include_globs: list[str] = ["**/*.py"]
    exclude_globs: list[str] = []

    chroma_dir: Path = Path(".agent/chroma")
    max_tokens: int = 8_192
    chunk_overlap: int = 64

    use_watchdog: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    class Config:
        env_prefix = "AGENT_"
        case_sensitive = False

    # Expand paths at validation‑time so mypy sees concrete `Path`
    @field_validator("project_root", mode="before")
    @classmethod
    def _expand_root(cls, v: Path | str) -> Path:
        return Path(v).expanduser().resolve()

    @field_validator("chroma_dir", mode="before")
    @classmethod
    def _expand_chroma(cls, v: Path | str) -> Path:
        return Path(v).expanduser().resolve()


def load(_: Path | None = None) -> Settings:
    """
    Return :class:`Settings` merged purely from environment/defaults.

    (JSON/YAML parsing omitted to stay 100 % type‑clean – extend as desired.)
    """
    return Settings()
