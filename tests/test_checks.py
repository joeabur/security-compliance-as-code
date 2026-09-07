from pathlib import Path

import pytest

from src.collectors.fixture import collect_fixture
from src.controls.checks import CHECKS


@pytest.fixture
def fixtures() -> tuple[dict, dict, dict]:
    root = Path("examples")
    return tuple(
        collect_fixture(root / name)
        for name in ("compliant.json", "partial.json", "non_compliant.json")
    )


@pytest.mark.parametrize("check_name", sorted(CHECKS))
def test_every_check_passes_compliant_fixture(
    check_name: str, fixtures: tuple[dict, dict, dict]
) -> None:
    passed, _ = CHECKS[check_name](fixtures[0])
    assert passed, check_name


@pytest.mark.parametrize("check_name", sorted(CHECKS))
def test_every_check_fails_non_compliant_fixture(
    check_name: str, fixtures: tuple[dict, dict, dict]
) -> None:
    passed, evidence = CHECKS[check_name](fixtures[2])
    assert not passed, evidence
