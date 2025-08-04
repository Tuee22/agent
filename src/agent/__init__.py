# src/agent/__init__.py
"""Top‑level package: exposes :class:`AgentConfig` and :class:`AgentSystem`."""

from importlib.metadata import version as _v

from .config import AgentConfig
from .core.system import AgentSystem

__all__: list[str] = ["AgentConfig", "AgentSystem", "__version__"]
__version__: str = _v(__name__)
