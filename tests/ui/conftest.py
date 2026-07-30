"""Selenium browser fixtures for UI tests."""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


def _path_without_chromedriver() -> str:
    """
    Remove PATH entries that contain a standalone chromedriver binary.

    Stale /usr/local/bin/chromedriver often mismatches installed Chrome;
    Selenium Manager then picks a compatible driver automatically.
    """
    parts = []
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        if not directory:
            continue
        driver_path = os.path.join(directory, "chromedriver")
        if os.path.isfile(driver_path):
            continue
        parts.append(directory)
    return os.pathsep.join(parts)


@pytest.fixture(scope="session")
def browser_options(request: pytest.FixtureRequest) -> Options:
    """Chrome options shared for the session; headless when --headless is passed."""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1920,1080")
    return options


@pytest.fixture(scope="function")
def driver(browser_options: Options):
    """
    Fresh Chrome WebDriver per test; quit after test completes.

    scope=function isolates tests — cart modal / navigation state does not leak.
    """
    path_backup = os.environ.get("PATH")
    try:
        os.environ["PATH"] = _path_without_chromedriver()
        chrome_driver = webdriver.Chrome(
            service=ChromeService(),
            options=browser_options,
        )
    finally:
        if path_backup is not None:
            os.environ["PATH"] = path_backup

    chrome_driver.implicitly_wait(10)
    yield chrome_driver
    chrome_driver.quit()
