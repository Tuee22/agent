from __future__ import annotations

from pathlib import Path

import typer
from typer import Typer

from ..config import load
from ..embeddings.indexer import HashEmbeddingClient, sync_all
from ..embeddings.store import get_store
from ..main import build_agent

app: Typer = Typer(add_completion=False, help="Code‑assistant CLI")


@app.command()
def index(config: Path | None = None) -> None:
    """Rebuild the local embedding index."""
    settings = load(config)
    store = get_store(settings.chroma_dir)
    sync_all(settings.project_root, store, HashEmbeddingClient())
    typer.echo("Index refreshed ✅")


@app.command()
def refactor(
    module: str,
    objective: str,
    config: Path | None = None,
) -> None:
    """
    Ask the agent to refactor *module* according to *objective*.
    (Demo – prints agent's response.)
    """
    settings = load(config)
    agent = build_agent(settings)
    msg = (
        f"Refactor the file `{module}`.  Objective: {objective}.\n"
        f"Apply best practices and ensure tests/type‑checks pass."
    )
    result = agent.chat_sync(msg)
    typer.echo(result.message.content)
