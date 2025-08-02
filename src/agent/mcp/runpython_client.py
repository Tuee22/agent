from dataclasses import dataclass


@dataclass(slots=True)
class MCPRunPythonClient:
    endpoint: str

    def run(self, code: str, timeout: int | None = None) -> str:
        raise NotImplementedError
