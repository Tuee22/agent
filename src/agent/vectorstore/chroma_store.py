# src/agent/vectorstore/chroma_store.py
"""ChromaDB backend."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import chromadb  # type: ignore
from chromadb import Settings

from .base import VectorStore


class ChromaStore(VectorStore):
    """Local (in‑mem) or persistent Chroma wrapper."""

    def __init__(self, persist: bool = False, path: Path | None = None) -> None:
        if persist:
            if path is None:
                raise ValueError("`path` must be supplied if persist=True.")
            path.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(path), settings=Settings())
        else:
            self._client = chromadb.Client(Settings())
        self._col = self._client.get_or_create_collection("code")

    # ------------------------------------------------------------------ #
    def add(self, texts: List[str], vectors: List[list[float]]) -> None:
        ids = [f"id{i}" for i in range(len(texts))]
        self._col.add(ids=ids, embeddings=vectors, documents=texts)

    def search(self, vector: list[float], k: int = 4) -> List[Tuple[str, float]]:
        q = self._col.query(query_embeddings=[vector], n_results=k)
        return list(zip(q["documents"][0], q["distances"][0]))
