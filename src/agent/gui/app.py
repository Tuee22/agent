"""Minimal FastAPI stub – extend with AG‑UI later."""
from fastapi import FastAPI

from ..config import load
from ..main import build_agent


def create_app() -> FastAPI:
    settings = load()
    build_agent(settings)
    return FastAPI(title="Agent GUI")
