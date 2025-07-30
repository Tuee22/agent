"""
core.py – minimal proof-of-concept for safe in-place self-modification.
"""
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]


def self_modify(edit_fn: Callable[[str], str], target: Path | None = None) -> None:
    """
    Apply *edit_fn* to the contents of *target* (defaults to this file).

    The real AI logic will live elsewhere; here we just provide:
    1. atomic write-back
    2. .bak safety copy
    """
    target = target or Path(__file__)
    original = target.read_text(encoding="utf-8")
    new_source = edit_fn(original)
    if new_source == original:
        print("No changes – file left intact.")
        return

    backup = target.with_suffix(target.suffix + ".bak")
    backup.write_text(original, encoding="utf-8")
    target.write_text(new_source, encoding="utf-8")
    print(f"🔄  Updated {target.relative_to(REPO_ROOT)} (backup → {backup.name})")
