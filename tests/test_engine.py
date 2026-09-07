from src.collectors.fixture import collect_fixture
from src.controls.loader import load_controls
from src.engine.evaluate import evaluate
from src.models import Status
from src.reporting.render import render_csv, render_html, render_json, render_markdown


def test_compliant_environment_passes_all_controls() -> None:
    report = evaluate(load_controls("controls"), collect_fixture("examples/compliant.json"))
    assert report.results
    assert all(result.status == Status.PASS for result in report.results)
    assert all(score == 100.0 for score in report.framework_scores().values())


def test_partial_environment_has_evidence_based_failures() -> None:
    report = evaluate(load_controls("controls"), collect_fixture("examples/partial.json"))
    failures = [result for result in report.results if result.status == Status.FAIL]
    assert failures
    assert all(result.evidence[0].message for result in failures)


def test_non_compliant_environment_fails() -> None:
    report = evaluate(load_controls("controls"), collect_fixture("examples/non_compliant.json"))
    assert any(result.status == Status.FAIL for result in report.results)


def test_report_formats_are_renderable() -> None:
    report = evaluate(load_controls("controls"), collect_fixture("examples/partial.json"))
    assert '"results"' in render_json(report)
    assert "control_id" in render_csv(report)
    assert "# Compliance Report" in render_markdown(report)
    assert "<table>" in render_html(report)
