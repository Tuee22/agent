# src/agent/util/files.py
"""Read/write helpers and unified‑diff patcher."""

from __future__ import annotations

import difflib
from pathlib import Path


def read(path: Path) -> str:
    """Read file as UTF‑8."""
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    """Write *text* to *path* atomically."""
    path.write_text(text, encoding="utf-8")


def apply_diff(path: Path, diff: str) -> str:
    """Apply *diff* (unified) to *path*, return resulting diff."""
    original = read(path).splitlines(keepends=True)
    patched = list(difflib.restore(diff.splitlines(keepends=True), 2))
    write(path, "".join(patched))
    udiff = difflib.unified_diff(original, patched, fromfile=str(path), tofile=str(path))
    return "".join(udiff)
