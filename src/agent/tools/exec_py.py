from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass


@dataclass(slots=True)
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str


def run_python(code: str, timeout: int | None = None) -> ExecResult:
    """Execute *code* in a temporary file."""
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as fh:
        fh.write(code)
        fh.flush()
        proc = subprocess.run(
            ["python", fh.name],
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    return ExecResult(proc.returncode, proc.stdout, proc.stderr)
