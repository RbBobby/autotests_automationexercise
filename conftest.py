"""
Root pytest hooks shared by API and UI suites.

  --headless  CLI flag for Chrome (used by tests/ui/conftest.py)
  Screenshot  saved to reports/screenshots/ on UI test failure
"""

from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register custom CLI options for the whole project."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser tests without a visible Chrome window",
    )


SCREENSHOTS_DIR = Path("reports/screenshots")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Capture browser screenshot when a UI test fails (needs driver fixture)."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = item.nodeid.replace("/", "_").replace("::", "__")
    screenshot_path = SCREENSHOTS_DIR / f"{safe_name}.png"
    try:
        driver.save_screenshot(str(screenshot_path))
        report.extra = getattr(report, "extra", [])
        report.extra.append(f"Screenshot: {screenshot_path}")
    except Exception:
        pass
