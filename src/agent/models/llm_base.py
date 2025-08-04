# src/agent/models/llm_base.py
"""LLM provider abstraction + OpenAI implementation."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, List

from openai import AsyncOpenAI  # type: ignore


class LLMBase(ABC):
    """Minimal interface every model provider must implement."""

    @abstractmethod
    async def acomplete(self, prompt: str) -> str:
        """Return completion text for *prompt* (async)."""


class OpenAIModel(LLMBase):
    """OpenAI Chat‑Completion backend."""

    def __init__(self, model: str, api_key: str | None = None, **kwargs: Any) -> None:
        self._client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._model = model
        self._kwargs: dict[str, Any] = kwargs

    async def acomplete(self, prompt: str) -> str:
        """Stream tokens then join to one string."""
        chunks: List[str] = []
        stream = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **self._kwargs,
        )
        async for part in stream:
            chunks.append(part.choices[0].delta.content or "")
        return "".join(chunks)
