from __future__ import annotations

import json
import math
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from secrets import token_hex
from typing import Final, List, Dict

EmbeddingVector = List[float]


@dataclass(slots=True)
class DocumentMatch:
    id: str
    text: str
    metadata: Dict[str, str]
    distance: float  # cosine distance (smaller = closer)


@dataclass(slots=True)
class _Record:
    id: str
    text: str
    embedding: EmbeddingVector
    metadata: Dict[str, str]


class VectorStore(ABC):
    """Minimal vector DB interface (sync)."""

    @abstractmethod
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[EmbeddingVector],
        metadatas: List[Dict[str, str]],
    ) -> List[str]:
        ...

    @abstractmethod
    def similarity_search(
        self,
        embedding: EmbeddingVector,
        k: int = 5,
    ) -> List[DocumentMatch]:
        ...

    @abstractmethod
    def upsert_document(
        self,
        id: str,
        text: str,
        embedding: EmbeddingVector,
        metadata: Dict[str, str],
    ) -> None:
        ...


class JsonVectorStore(VectorStore):
    """Self‑contained JSONL‑persisted implementation (no external deps)."""

    _STORE_FILE: Final[str] = "vectors.jsonl"

    def __init__(self, persist_dir: Path) -> None:
        self._dir = persist_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._records: Dict[str, _Record] = {}
        self._load()

    # ---------------------------- public API ---------------------------- #
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[EmbeddingVector],
        metadatas: List[Dict[str, str]],
    ) -> List[str]:
        ids: List[str] = []
        for text, emb, meta in zip(texts, embeddings, metadatas):
            doc_id = token_hex(8)
            self._records[doc_id] = _Record(doc_id, text, emb, meta)
            ids.append(doc_id)
        self._flush()
        return ids

    def similarity_search(
        self, embedding: EmbeddingVector, k: int = 5
    ) -> List[DocumentMatch]:
        def cosine(a: EmbeddingVector, b: EmbeddingVector) -> float:
            num = sum(x * y for x, y in zip(a, b))
            denom = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
            return 1.0 - num / denom if denom else 1.0

        scored = [(rec, cosine(rec.embedding, embedding)) for rec in self._records.values()]
        scored.sort(key=lambda t: t[1])
        return [
            DocumentMatch(r.id, r.text, r.metadata, dist) for r, dist in scored[:k]
        ]

    def upsert_document(
        self,
        id: str,
        text: str,
        embedding: EmbeddingVector,
        metadata: Dict[str, str],
    ) -> None:
        self._records[id] = _Record(id, text, embedding, metadata)
        self._flush()

    # --------------------------- persistence --------------------------- #
    def _path(self) -> Path:
        return self._dir / self._STORE_FILE

    def _load(self) -> None:
        if not self._path().exists():
            return
        with self._path().open("r", encoding="utf-8") as fh:
            for line in fh:
                raw = json.loads(line)
                self._records[raw["id"]] = _Record(
                    raw["id"],
                    raw["text"],
                    [float(x) for x in raw["embedding"]],
                    {str(k): str(v) for k, v in raw["metadata"].items()},
                )

    def _flush(self) -> None:
        tmp = self._path().with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            for rec in self._records.values():
                fh.write(
                    json.dumps(
                        {
                            "id": rec.id,
                            "text": rec.text,
                            "embedding": rec.embedding,
                            "metadata": rec.metadata,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        tmp.replace(self._path())


def get_store(persist_dir: Path) -> VectorStore:
    return JsonVectorStore(persist_dir)
