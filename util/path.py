from os import path
from pathlib import Path


def normalize_path(file_path: Path | str) -> Path:
    """Normalizes a file path, with tilde and variable expansion."""
    return Path(path.expandvars(path.expanduser(file_path)))
