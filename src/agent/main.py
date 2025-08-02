from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent, tool

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
    """
    Initialise and return a :class:`pydantic_ai.Agent` with all tools wired up.
    """
    store = get_store(settings.chroma_dir)
    deps = Deps(settings, store, settings.project_root)
    agent = Agent(
        name="code‑agent",
        system_message=(
            "You are a type‑safe, test‑driven coding assistant. "
            "Prefer correctness, readability, and small diffs."
        ),
        deps_type=Deps,
        deps=deps,
    )

    client = HashEmbeddingClient()  # deterministic offline embedder

    # ---------------------------  tool wrappers  ------------------------- #
    @agent.tool
    def search_code(query: str, k: int = 5) -> str:
        snippets = code_search(query, k, deps.vector_store, client)
        return "\n\n---\n\n".join(s.code for s in snippets)

    # File ops
    agent.register_tool(read_file)

    @agent.tool(name="write_file")
    def _write_file(path: str, content: str) -> str:
        return write_file(path, content, deps.vector_store, client)

    # Validation
    agent.register_tool(run_tests)
    agent.register_tool(run_mypy)
    agent.register_tool(run_python)

    return agent
