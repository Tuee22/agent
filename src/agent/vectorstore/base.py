# src/agent/vectorstore/base.py
"""Tiny interface for semantic search."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple


class VectorStore(ABC):
    """Add/query embeddings."""

    @abstractmethod
    def add(self, texts: List[str], vectors: List[list[float]]) -> None: ...

    @abstractmethod
    def search(self, vector: list[float], k: int = 4) -> List[Tuple[str, float]]: ...
