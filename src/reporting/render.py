"""JSON, CSV, Markdown, and HTML report renderers."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict
from html import escape
from typing import Any

from src.models import ComplianceReport


def report_dict(report: ComplianceReport) -> dict[str, Any]:
    return {
        "generated_at": report.generated_at,
        "framework_scores": report.framework_scores(),
        "results": [
            {
                "control_id": r.control_id,
                "framework": r.framework,
                "status": r.status.value,
                "severity": r.severity,
                "requirement": r.requirement,
                "recommendation": r.recommendation,
                "owner": r.owner,
                "remediation": r.remediation,
                "evidence": [asdict(e) for e in r.evidence],
                "exception": r.exception,
            }
            for r in report.results
        ],
        "risk_summary": {
            "failed_controls": sum(r.status.value == "FAIL" for r in report.results),
            "note": "Compliance does not guarantee security.",
        },
    }


def render_json(report: ComplianceReport) -> str:
    return json.dumps(report_dict(report), indent=2)


def render_csv(report: ComplianceReport) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["control_id", "framework", "status", "severity", "evidence", "recommendation"],
    )
    writer.writeheader()
    for result in report.results:
        writer.writerow(
            {
                "control_id": result.control_id,
                "framework": result.framework,
                "status": result.status.value,
                "severity": result.severity,
                "evidence": "; ".join(e.message for e in result.evidence),
                "recommendation": result.recommendation,
            }
        )
    return output.getvalue()


def render_markdown(report: ComplianceReport) -> str:
    lines = [
        "# Compliance Report",
        "",
        f"Generated: {report.generated_at}",
        "",
        "## Framework Scores",
        "",
    ]
    lines += [
        f"- **{framework}**: {score}%" for framework, score in report.framework_scores().items()
    ]
    lines += [
        "",
        "## Control Results",
        "",
        "| Control | Framework | Status | Severity | Evidence |",
        "|---|---|---|---|---|",
    ]
    lines += [
        "| {control} | {framework} | {status} | {severity} | {evidence} |".format(
            control=r.control_id,
            framework=r.framework,
            status=r.status.value,
            severity=r.severity,
            evidence="; ".join(e.message for e in r.evidence),
        )
        for r in report.results
    ]
    lines += ["", "> Compliance does not guarantee security."]
    return "\n".join(lines) + "\n"


def render_html(report: ComplianceReport) -> str:
    rows = "".join(
        "<tr><td>{control}</td><td>{framework}</td><td>{status}</td>"
        "<td>{severity}</td><td>{evidence}</td></tr>".format(
            control=escape(r.control_id),
            framework=escape(r.framework),
            status=r.status.value,
            severity=escape(r.severity),
            evidence=escape("; ".join(e.message for e in r.evidence)),
        )
        for r in report.results
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Compliance Report</title></head><body>"
        "<h1>Compliance Report</h1>"
        "<p>Compliance does not guarantee security.</p><table>"
        "<tr><th>Control</th><th>Framework</th><th>Status</th>"
        f"<th>Severity</th><th>Evidence</th></tr>{rows}</table>"
        "</body></html>"
    )
