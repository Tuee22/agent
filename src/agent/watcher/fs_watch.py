"""
Polling watcher to keep vector store in sync without external deps.
"""
from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Dict

from ..embeddings.indexer import EmbeddingClient, file_sha1, reembed_file
from ..embeddings.store import VectorStore


def _snapshot(root: Path) -> Dict[Path, str]:
    return {p: file_sha1(p) for p in root.rglob("*.py")}


def start_watcher(
    root: Path,
    store: VectorStore,
    client: EmbeddingClient,
    interval: float = 1.0,
) -> threading.Thread:
    """Return a daemon thread that re‑indexes changed files."""
    state = _snapshot(root)

    def loop() -> None:
        while True:
            time.sleep(interval)
            nxt = _snapshot(root)
            for path, digest in nxt.items():
                if state.get(path) != digest:
                    reembed_file(path, store, client)
            state.update(nxt)

    t = threading.Thread(target=loop, name="agent-fs-watch", daemon=True)
    t.start()
    return t
