from __future__ import annotations

from pathlib import Path
from typing import List

import typer
from typer import Typer

from ..config import load
from ..embeddings.indexer import HashEmbeddingClient, sync_all
from ..embeddings.store import get_store
from ..main import build_agent

app: Typer = Typer(add_completion=False, help="Code‑assistant CLI")


@app.command()
def index(config: Path | None = None) -> None:
    """(Re)build the local embedding index."""
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
    """Ask the agent to refactor *module* with *objective*."""
    settings = load(config)
    agent = build_agent(settings)
    prompt = (
        f"Refactor the file `{module}`. Objective: {objective}. "
        "Ensure tests and type‑checks pass."
    )
    reply = agent.chat_sync(prompt)
    typer.echo(reply.message.content)
