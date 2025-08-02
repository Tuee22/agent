from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Final, List, Sequence

import chromadb
from chromadb.config import Settings as ChromaSettings

# ------------------------------------------------------------
# Types
# ------------------------------------------------------------
EmbeddingVector = List[float]

@dataclass(slots=True)
class DocumentMatch:
    id: str
    text: str
    metadata: Dict[str, str]
    distance: float    # cosine distance (smaller == closer)

@dataclass(slots=True)
class _Record:
    id: str
    text: str
    embedding: EmbeddingVector
    metadata: Dict[str, str]

# ------------------------------------------------------------
# Abstract interface (unchanged)
# ------------------------------------------------------------
class VectorStore(ABC):
    @abstractmethod
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[EmbeddingVector],
        metadatas: List[Dict[str, str]],
    ) -> List[str]: ...

    @abstractmethod
    def similarity_search(
        self, embedding: EmbeddingVector, k: int = 5
    ) -> List[DocumentMatch]: ...

    @abstractmethod
    def upsert_document(
        self,
        id: str,
        text: str,
        embedding: EmbeddingVector,
        metadata: Dict[str, str],
    ) -> None: ...

    @abstractmethod
    def get_document(self, id: str) -> _Record | None: ...

# ------------------------------------------------------------
# Concrete Chroma implementation
# ------------------------------------------------------------
class ChromaVectorStore(VectorStore):
    """
    Vector store backed by ChromaDB.

    * Persistent mode*  – pass a directory path (default `.agent/chroma`)
    * In‑memory mode*   – pass ``None`` *or* set `AGENT_CHROMA_DIR=:memory:`
    """

    _COLLECTION: Final[str] = "agent"

    def __init__(self, persist_dir: Path | None) -> None:
        chroma_cfg = ChromaSettings(
            is_persistent=bool(persist_dir),
            persist_directory=str(persist_dir) if persist_dir else None,
        )
        self._client = chromadb.Client(chroma_cfg)
        self._col = self._client.get_or_create_collection(self._COLLECTION)

    # ------------- VectorStore API ------------- #
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[EmbeddingVector],
        metadatas: List[Dict[str, str]],
    ) -> List[str]:
        ids = [self._col.count() + i for i in range(len(texts))]
        str_ids = [str(x) for x in ids]
        self._col.add(
            ids=str_ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return str_ids

    def upsert_document(
        self,
        id: str,
        text: str,
        embedding: EmbeddingVector,
        metadata: Dict[str, str],
    ) -> None:
        self._col.upsert(
            ids=[id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def similarity_search(
        self, embedding: EmbeddingVector, k: int = 5
    ) -> List[DocumentMatch]:
        q = self._col.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["ids", "distances", "documents", "metadatas"],
        )
        ids = q["ids"][0]
        dists = q["distances"][0]
        docs = q["documents"][0]
        metas = q["metadatas"][0]
        return [
            DocumentMatch(i, doc, meta, dist)
            for i, doc, meta, dist in zip(ids, docs, metas, dists)
        ]

    def get_document(self, id: str) -> _Record | None:
        res = self._col.get(ids=[id], include=["documents", "embeddings", "metadatas"])
        if not res["ids"]:
            return None
        return _Record(
            id=res["ids"][0],
            text=res["documents"][0],
            embedding=res["embeddings"][0],
            metadata=res["metadatas"][0],
        )

# ------------------------------------------------------------
# Factory used throughout the code‑base
# ------------------------------------------------------------
def get_store(persist_dir: Path | str) -> VectorStore:
    """
    Return a VectorStore.

    • ``persist_dir == ':memory:'`` (string) → in‑memory
    • Any other truthy path                    → persistent on disk
    """
    if str(persist_dir) == ":memory:":
        return ChromaVectorStore(None)
    return ChromaVectorStore(Path(persist_dir))
