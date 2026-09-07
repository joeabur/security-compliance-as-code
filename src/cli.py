"""Command-line interface for compliance evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.collectors.fixture import collect_fixture
from src.controls.loader import load_controls
from src.engine.evaluate import evaluate
from src.reporting.render import render_csv, render_html, render_json, render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate AWS/Terraform configuration against compliance controls"
    )
    parser.add_argument("--config", required=True, help="Path to normalized configuration JSON")
    parser.add_argument(
        "--controls", default="controls", help="Directory containing framework YAML controls"
    )
    parser.add_argument("--format", choices=["json", "csv", "markdown", "html"], default="json")
    parser.add_argument("--output", default="-", help="Output file, or - for stdout")
    args = parser.parse_args()
    report = evaluate(load_controls(args.controls), collect_fixture(args.config))
    rendered = {
        "json": render_json,
        "csv": render_csv,
        "markdown": render_markdown,
        "html": render_html,
    }[args.format](report)
    if args.output == "-":
        print(rendered)
    else:
        Path(args.output).write_text(rendered, encoding="utf-8")
    return 1 if any(result.status.value in {"FAIL", "ERROR"} for result in report.results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
