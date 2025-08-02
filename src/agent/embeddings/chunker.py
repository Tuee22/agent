"""
Token‑agnostic code chunker: splits source by **line count** with overlap.
"""
from __future__ import annotations

from collections.abc import Iterable


def _chunks(lines: list[str], size: int, overlap: int) -> Iterable[list[str]]:
    start: int = 0
    total = len(lines)
    while start < total:
        end = min(start + size, total)
        yield lines[start:end]
        if end == total:
            break
        start = end - overlap


def chunk_code(code: str, max_lines: int = 400, overlap: int = 40) -> list[str]:
    """
    Return overlapping line‑chunks.  Defaults ≈800 GPT‑4 tokens w/ context.
    """
    lines = code.splitlines(keepends=True)
    return ["".join(block) for block in _chunks(lines, max_lines, overlap)]
