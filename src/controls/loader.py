"""Load normalized controls from YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.models import Control


def load_controls(directory: str | Path) -> list[Control]:
    controls: list[Control] = []
    for path in sorted(Path(directory).rglob("*.yaml")):
        with path.open(encoding="utf-8") as handle:
            records: list[dict[str, Any]] = yaml.safe_load(handle) or []
        controls.extend(Control(**record) for record in records)
    return controls
