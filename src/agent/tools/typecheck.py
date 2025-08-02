from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final, List, Sequence


@dataclass(slots=True)
class MypyResult:
    success: bool
    error_count: int
    stdout: str


_ERROR: Final[re.Pattern[str]] = re.compile(r"Found (?P<n>\\d+) errors? in")


def run_mypy(
    paths: Sequence[Path] | None = None,
    strict: bool = False,
) -> MypyResult:
    cmd: List[str] = ["mypy", *(["--strict"] if strict else []), *(p.as_posix() for p in paths or [Path(".")])]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    out = proc.stdout + proc.stderr
    m = _ERROR.search(out)
    n_errors = int(m.group("n")) if m else 0
    return MypyResult(proc.returncode == 0, n_errors, out)
