from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


@dataclass(slots=True)
class MCPFilesystemClient:
    """Local stand‑in for an MCP filesystem server."""
    endpoint: str = "local"

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write_file(self, path: Path, content: str) -> str:
        path.write_text(content, encoding="utf-8")
        return "written"

    def list_files(self, globs: Sequence[str]) -> List[Path]:
        root = Path(".").resolve()
        out: List[Path] = []
        for pattern in globs:
            out.extend(root.glob(pattern))
        return out
