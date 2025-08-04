# src/agent/embeddings/openai_embed.py
"""OpenAI embeddings."""

from __future__ import annotations

import os
from typing import Iterable, List

from openai import AsyncOpenAI  # type: ignore

from .base import Embedder


class OpenAIEmbedder(Embedder):
    """Wrapper around OpenAI embedding endpoint."""

    def __init__(self, model: str, api_key: str | None = None) -> None:
        self._client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._model = model

    async def aembed(self, texts: Iterable[str]) -> List[list[float]]:
        resp = await self._client.embeddings.create(model=self._model, input=list(texts))
        return [d.embedding for d in resp.data]
