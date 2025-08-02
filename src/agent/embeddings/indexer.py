from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Protocol, TypedDict, List

from .chunker import chunk_code
from .store import EmbeddingVector, VectorStore


class EmbeddingClient(Protocol):
    """Very small contract for an embedder."""

    def embed(self, text: str) -> EmbeddingVector: ...


class HashEmbeddingClient:
    """
    Deterministic, offline embedder: converts SHA‑256 digest into fixed‑length
    vector.  Replace with OpenAI when online.
    """

    _DIM: int = 128

    def embed(self, text: str) -> EmbeddingVector:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        raw = (digest * (self._DIM // len(digest) + 1))[: self._DIM]
        return [byte / 255.0 for byte in raw]


class _Meta(TypedDict):
    file_path: str
    start_line: int
    end_line: int
    file_sha1: str


def file_sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def _vector_id(path: Path, idx: int) -> str:
    return f"{path}:{idx}"


def reembed_file(path: Path, store: VectorStore, client: EmbeddingClient) -> None:
    sha1 = file_sha1(path)
    chunks = chunk_code(path.read_text(encoding="utf-8"))
    start_line = 0
    for idx, chunk in enumerate(chunks):
        lines = chunk.count("\n")
        meta: _Meta = {
            "file_path": str(path),
            "start_line": start_line + 1,
            "end_line": start_line + lines,
            "file_sha1": sha1,
        }
        store.upsert_document(
            _vector_id(path, idx),
            chunk,
            client.embed(chunk),
            meta,  # type: ignore[arg-type]
        )
        start_line += lines


def reembed_ids(
    ids: List[str], store: VectorStore, client: EmbeddingClient
) -> None:
    # Minimal placeholder: full implementation not required for baseline.
    return None


def sync_all(root: Path, store: VectorStore, client: EmbeddingClient) -> None:
    for path in root.rglob("*.py"):
        reembed_file(path, store, client)
