from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, List


@dataclass(slots=True)
class MCPFilesystemClient:
    endpoint: str

    def read_file(self, path: Path) -> str:
        raise NotImplementedError

    def write_file(self, path: Path, content: str) -> str:
        raise NotImplementedError

    def list_files(self, globs: Sequence[str]) -> List[Path]:
        raise NotImplementedError
