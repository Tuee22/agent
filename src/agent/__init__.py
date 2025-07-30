"""agent – self-modifying, Pydantic-AI powered code assistant."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("agent")
except PackageNotFoundError:  # running from source tree
    __version__ = "0.0.0.dev0"

__all__ = ["__version__"]
