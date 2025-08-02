"""CLI entry‑point for Poetry."""
from .app import app


def main() -> None:  # Poetry calls this
    app()
