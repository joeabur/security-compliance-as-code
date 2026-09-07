"""Compliance evaluation orchestration."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from src.controls.checks import CHECKS
from src.models import ComplianceReport, Control, ControlResult, Evidence, Status


def evaluate(controls: list[Control], config: dict[str, Any]) -> ComplianceReport:
    results: list[ControlResult] = []
    for control in controls:
        try:
            passed, message = CHECKS[control.check](config)
            status = Status.PASS if passed else Status.FAIL
            evidence = [Evidence(message=message, details={"check": control.check})]
        except KeyError:
            status = Status.ERROR
            evidence = [Evidence(message=f"Unknown check: {control.check}", source="engine")]
        results.append(
            ControlResult(
                control_id=control.control_id,
                framework=control.framework,
                status=status,
                severity=control.severity,
                requirement=control.requirement,
                recommendation=control.recommendation,
                owner=control.owner,
                remediation=control.remediation,
                evidence=evidence,
            )
        )
    return ComplianceReport(generated_at=datetime.now(UTC).isoformat(), results=results)
