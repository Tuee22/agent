from dataclasses import dataclass
from subprocess import run
from typing import Sequence


@dataclass(slots=True)
class MCPRunPythonClient:
    """Execute Python via subprocess (local MCP stand‑in)."""
    endpoint: str = "local"

    def run(self, code: str, timeout: int | None = None) -> str:
        proc = run(
            ["python", "- <<'PY'\n" + code + "\nPY"],
            text=True,
            capture_output=True,
            timeout=timeout,
            shell=True,  # heredoc requires shell
        )
        return proc.stdout + proc.stderr
