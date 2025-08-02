from __future__ import annotations

import hashlib
from pathlib import Path
from typing import List, Protocol

from .chunker import chunk_code
from .store import EmbeddingVector, VectorStore


class EmbeddingClient(Protocol):
    def embed(self, text: str) -> EmbeddingVector: ...


class HashEmbeddingClient:
    """Deterministic offline embedder (SHA‑256 → 128‑D)."""

    _DIM = 128

    def embed(self, text: str) -> EmbeddingVector:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        raw = (digest * (self._DIM // len(digest) + 1))[: self._DIM]
        return [b / 255.0 for b in raw]


def file_sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def _vid(path: Path, idx: int) -> str:
    return f"{path}:{idx}"


def reembed_file(path: Path, store: VectorStore, client: EmbeddingClient) -> None:
    sha1 = file_sha1(path)
    chunks = chunk_code(path.read_text(encoding="utf-8"))
    start_line = 0
    for idx, chunk in enumerate(chunks):
        lines = chunk.count("\n")
        meta = {
            "file_path": str(path),
            "start_line": str(start_line + 1),
            "end_line": str(start_line + lines),
            "file_sha1": sha1,
        }
        store.upsert_document(_vid(path, idx), chunk, client.embed(chunk), meta)
        start_line += lines


def reembed_ids(ids: List[str], store: VectorStore, client: EmbeddingClient) -> None:
    """Refresh vectors given their IDs by re‑embedding the full file."""
    for _id in ids:
        path_str = _id.split(":", 1)[0]
        reembed_file(Path(path_str), store, client)


def sync_all(root: Path, store: VectorStore, client: EmbeddingClient) -> None:
    for path in root.rglob("*.py"):
        reembed_file(path, store, client)
