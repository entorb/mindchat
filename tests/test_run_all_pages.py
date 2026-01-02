"""Test: Open all Pages/Reports."""  # noqa: INP001

# ruff: noqa: D103
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


# helpers
def init_report(path: Path) -> AppTest:
    at = AppTest.from_file(str(path))
    # setup some session variables
    at.session_state["logged_in"] = True
    return at


def run_and_assert_no_problems(at: AppTest, path: Path, timeout: int = 300) -> None:
    at.run(timeout=timeout)
    assert not at.exception, path.stem + ": " + str(at.exception)
    assert not at.error, path.stem + ": " + str(at.error)
    assert not at.warning, path.stem + ": " + str(at.warning)


def init_and_run(path: Path, timeout: int = 300) -> AppTest:
    at = init_report(path)
    run_and_assert_no_problems(at, path, timeout=timeout)
    return at


pages = sorted(Path("src/reports").glob("*.py"))


@pytest.mark.parametrize("p", pages)
def test_all_pages(p: Path) -> None:
    """Open all pages and check for errors and warnings."""
    _ = init_and_run(p)
