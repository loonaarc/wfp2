"""Provenance capture for reproducible experiments.

Every exported experiment records enough context to reproduce it: the software
version and git commit, the Python/platform, a timestamp, the seeds, and the run
status. This is what turns "I ran a simulation" into "here is a run anyone can
re-execute and compare against."
"""

from __future__ import annotations

import platform
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .. import __version__


def _git_commit() -> str | None:
    """Return the current git commit hash, or ``None`` if unavailable."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).resolve().parent,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


@dataclass
class Provenance:
    """Reproducibility metadata attached to an experiment's outputs."""

    package_version: str = field(default_factory=lambda: __version__)
    git_commit: str | None = field(default_factory=_git_commit)
    python_version: str = field(default_factory=platform.python_version)
    platform: str = field(default_factory=platform.platform)
    timestamp_utc: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    seeds: tuple[int, ...] = ()
    status: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""
        return asdict(self)
