from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent

from .config import Settings
from .deps import Deps
from .embeddings.indexer import HashEmbeddingClient
from .embeddings.store import get_store
from .tools import (
    code_search,
    read_file,
    run_mypy,
    run_python,
    run_tests,
    write_file,
)


def build_agent(settings: Settings) -> Agent:
    """Create and wire a Pydantic AI agent."""
    store = get_store(settings.chroma_dir)
    deps = Deps(settings, store, settings.project_root)
    agent = Agent(
        name="code‑agent",
        system_message=(
            "You are a type‑safe coding assistant. "
            "Refactor code, ensure tests and mypy strict pass."
        ),
        deps_type=Deps,
        deps=deps,
    )

    embedder = HashEmbeddingClient()
    # Automatically refresh vectors when Python files change
    from .watcher import start_watcher
    start_watcher(settings.project_root, store, embedder)

    # -------- tools -------- #
    agent.register_tool(read_file)

    @agent.tool(name="write_file")
    def _write(path: str, content: str) -> str:
        return write_file(path, content, store, embedder)

    @agent.tool
    def search_code(query: str, k: int = 5) -> str:
        snippets = code_search(query, k, store, embedder)
        return "\n\n---\n\n".join(s.code for s in snippets)

    agent.register_tool(run_tests)
    agent.register_tool(run_mypy)
    agent.register_tool(run_python)
    return agent
