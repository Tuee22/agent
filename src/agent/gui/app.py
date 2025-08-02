"""
Placeholder FastAPI GUI – kept minimal to stay dependency‑light.
"""

from fastapi import FastAPI

from ..config import load
from ..main import build_agent


def create_app() -> FastAPI:
    settings = load()
    build_agent(settings)  # ensure tools/agent initialised
    return FastAPI(title="Agent GUI")
