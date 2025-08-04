# src/agent/core/executor.py
"""Run shell commands in‑process or inside Docker."""

from __future__ import annotations

import asyncio
import shutil
from pathlib import Path
from typing import List, Sequence, Tuple

from ..config import ExecutionConfig


class Executor:
    """Wrapper around subprocess/Docker with timeout enforcement."""

    def __init__(self, cfg: ExecutionConfig, root: Path) -> None:
        self._cfg = cfg
        self._root = root

    # ------------------------------------------------------------------ #
    async def arun(self, cmd: Sequence[str]) -> Tuple[int, str, str]:
        """Return (exit‑code, stdout, stderr)."""
        if self._cfg.use_docker:
            return await self._arun_docker(cmd)
        return await self._arun_local(cmd)

    # Local ------------------------------------------------------------- #
    async def _arun_local(self, cmd: Sequence[str]) -> Tuple[int, str, str]:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=self._root,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), self._cfg.timeout)
        except asyncio.TimeoutError:
            proc.kill()
            return 124, "", "TIMEOUT"
        return proc.returncode, stdout.decode(), stderr.decode()

    # Docker ------------------------------------------------------------ #
    async def _arun_docker(self, cmd: Sequence[str]) -> Tuple[int, str, str]:
        if shutil.which("docker") is None:
            return 127, "", "Docker not found."
        full = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{self._root}:/workspace",
            "-w",
            "/workspace",
            self._cfg.image,
            *cmd,
        ]
        return await self._arun_local(full)
