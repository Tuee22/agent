from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List


@dataclass(slots=True)
class MCPGitClient:
    """Thin wrapper around the local *git* CLI (acts like an MCP client)."""
    endpoint: str = "local"
    repo_root: Path = Path(".").resolve()

    def _cmd(self, *args: str) -> str:
        try:
            result = run(
                ["git", "-C", str(self.repo_root), *args],
                text=True,
                capture_output=True,
                check=True,
            )
            return result.stdout
        except CalledProcessError as exc:
            return exc.stderr

    def diff(self, path: Path | None = None) -> str:
        return self._cmd("diff", "--", str(path)) if path else self._cmd("diff")

    def commit(self, message: str) -> str:
        return self._cmd("commit", "-am", message)

    def checkout(self, branch: str, create: bool = False) -> str:
        args: List[str] = ["checkout"]
        if create:
            args.extend(["-b", branch])
        else:
            args.append(branch)
        return self._cmd(*args)
