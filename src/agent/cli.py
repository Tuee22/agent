"""
Small CLI stub exposed as the `agent` command.
"""
import argparse
from pathlib import Path

from . import __version__


def _info(_args):
    print(f"agent v{__version__}")
    print(f"Current working dir: {Path.cwd()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Pydantic-AI powered, self-modifying coding assistant (stub).",
    )
    parser.set_defaults(func=_info)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
