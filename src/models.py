"""Normalized compliance domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Status(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ERROR = "ERROR"


@dataclass(slots=True)
class Control:
    control_id: str
    framework: str
    requirement: str
    description: str
    severity: str
    check: str
    recommendation: str
    owner: str
    remediation: str
    references: list[str] = field(default_factory=list)
    mappings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Evidence:
    message: str
    source: str = "fixture"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ControlResult:
    control_id: str
    framework: str
    status: Status
    severity: str
    requirement: str
    recommendation: str
    owner: str
    remediation: str
    evidence: list[Evidence] = field(default_factory=list)
    exception: dict[str, Any] | None = None


@dataclass(slots=True)
class ComplianceReport:
    generated_at: str
    results: list[ControlResult]
    risk_acceptances: list[dict[str, Any]] = field(default_factory=list)

    def framework_scores(self) -> dict[str, float]:
        grouped: dict[str, list[ControlResult]] = {}
        for result in self.results:
            grouped.setdefault(result.framework, []).append(result)
        scores: dict[str, float] = {}
        for framework, results in grouped.items():
            applicable = [r for r in results if r.status != Status.NOT_APPLICABLE]
            scores[framework] = (
                round(sum(r.status == Status.PASS for r in applicable) / len(applicable) * 100, 2)
                if applicable
                else 100.0
            )
        return scores
