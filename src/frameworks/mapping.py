"""Framework mappings are directional references, not equivalence claims."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import yaml


def load_mappings(path: str | Path) -> dict[str, list[dict[str, Any]]]:
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return cast(dict[str, list[dict[str, Any]]], data.get("mappings", {}))
