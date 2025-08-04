# src/agent/embeddings/base.py
"""Abstract embedder."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List


class Embedder(ABC):
    """Return vector representations for text."""

    @abstractmethod
    async def aembed(self, texts: Iterable[str]) -> List[list[float]]:
        """Async embedding call."""
