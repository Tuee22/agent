# src/agent/cli.py
"""`agent` CLI entry‑point."""

from __future__ import annotations

import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Tuple

from .config import AgentConfig
from .core.system import AgentSystem


def _parse_models(raw: list[str] | None) -> Dict[str, Tuple[str, str]]:
    mapping: Dict[str, Tuple[str, str]] = {}
    if raw:
        for spec in raw:
            role, provider, model = spec.split(":", 2)
            mapping[role] = (provider, model)
    return mapping


def main() -> None:
    parser = ArgumentParser(description="AutoGen multipurpose code‑assistant.")
    parser.add_argument("--path", required=True, help="Target code folder.")
    parser.add_argument(
        "--pipeline",
        choices=["refactor", "docs", "test", "validate"],
        default="refactor",
    )
    parser.add_argument(
        "--model",
        action="append",
        help="role:provider:model (repeatable). Example: coder:openai:gpt-4o",
    )
    parser.add_argument("prompt", help="Task for the agents.")
    ns = parser.parse_args()

    cfg = AgentConfig(
        project_path=Path(ns.path).resolve(),
        model_providers=_parse_models(ns.model)
        or {
            "coder": ("openai", "gpt-4o"),
            "tester": ("openai", "gpt-4o"),
            "reviewer": ("openai", "gpt-4o"),
        },
        provider_configs={"openai": {"api_key": os.getenv("OPENAI_API_KEY")}},
        embedding_provider=("openai", "text-embedding-3-small"),
    )
    AgentSystem(cfg).run_pipeline(ns.pipeline, ns.prompt)


if __name__ == "__main__":
    main()
