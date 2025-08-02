from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .embeddings.store import VectorStore


@dataclass(slots=True)
class Deps:
    """Resolved singletons injected into the Agent."""
    settings: Settings
    vector_store: VectorStore
    project_root: Path
