"""Public API surface for *agent*."""
from pathlib import Path
from typing import Final

from pydantic_ai import Agent

from .config import load
from .main import build_agent

__all__: Final[list[str]] = ["get_agent"]


def get_agent(config_file: Path | None = None) -> Agent:
    """Return a fully‑configured :class:`pydantic_ai.Agent` instance."""
    settings = load(config_file)
    return build_agent(settings)
