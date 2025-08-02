from pathlib import Path

from agent import get_agent


def test_agent_loads(tmp_path: Path) -> None:
    agent = get_agent()
    assert agent.name == "code‑agent"
