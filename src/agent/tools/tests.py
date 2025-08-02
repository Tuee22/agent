from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Sequence, Iterable, List


@dataclass(slots=True)
class TestResult:
    passed: bool
    failed_count: int
    output: str


_SUMMARY_RE: Final[re.Pattern[str]] = re.compile(
    r"=+\\s*(?P<passed>\\d+) passed.*?(?P<failed>\\d+) failed|"
    r"=+\\s*(?P<passed_only>\\d+) passed in",
    re.I | re.S,
)


def _pytest_cmd(paths: Iterable[Path], extra: Sequence[str]) -> List[str]:
    return ["pytest", *[str(p) for p in paths], *extra]


def run_tests(
    paths: Sequence[Path] | None = None,
    pytest_args: Sequence[str] | None = None,
) -> TestResult:
    paths = list(paths or [Path(".")])
    extra = list(pytest_args or [])
    proc = subprocess.run(
        _pytest_cmd(paths, extra),
        text=True,
        capture_output=True,
    )
    output = proc.stdout + proc.stderr
    m = _SUMMARY_RE.search(output)
    if m is None:
        return TestResult(False, 1, output)
    if m.group("passed_only") is not None:
        return TestResult(True, 0, output)
    failed = int(m.group("failed") or "0")
    return TestResult(failed == 0, failed, output)
