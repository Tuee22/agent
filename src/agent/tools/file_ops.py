from pathlib import Path

from ..embeddings.indexer import EmbeddingClient, reembed_file
from ..embeddings.store import VectorStore


def read_file(path: str) -> str:
    """Return UTF‑8 contents of *path*."""
    return Path(path).read_text(encoding="utf-8")


def write_file(
    path: str,
    content: str,
    store: VectorStore,
    client: EmbeddingClient,
) -> str:
    """Write *content* then refresh its vectors."""
    p = Path(path)
    p.write_text(content, encoding="utf-8")
    reembed_file(p, store, client)
    return "written"
