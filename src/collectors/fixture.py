"""Offline collector for AWS/Terraform normalized snapshots."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def collect_fixture(path: str | Path) -> dict[str, Any]:
    """Load a normalized infrastructure snapshot from JSON."""
    with Path(path).open(encoding="utf-8") as handle:
        data: dict[str, Any] = json.load(handle)
    return data
