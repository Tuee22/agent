from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MCPGitClient:
    endpoint: str
    repo_root: Path

    def diff(self, path: Path | None = None) -> str:
        raise NotImplementedError

    def commit(self, message: str) -> str:
        raise NotImplementedError

    def checkout(self, branch: str, create: bool = False) -> str:
        raise NotImplementedError
