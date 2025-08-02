from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..embeddings.indexer import EmbeddingClient
from ..embeddings.store import DocumentMatch, VectorStore


@dataclass(slots=True)
class CodeSnippet:
    file_path: str
    start_line: int
    end_line: int
    code: str
    score: float


def code_search(
    query: str,
    k: int,
    store: VectorStore,
    client: EmbeddingClient,
) -> List[CodeSnippet]:
    emb = client.embed(query)
    matches: List[DocumentMatch] = store.similarity_search(emb, k=k)
    return [
        CodeSnippet(
            file_path=m.metadata["file_path"],
            start_line=int(m.metadata["start_line"]),
            end_line=int(m.metadata["end_line"]),
            code=m.text,
            score=m.distance,
        )
        for m in matches
    ]
