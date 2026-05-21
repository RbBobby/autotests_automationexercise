import os

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


def _path_without_chromedriver() -> str:
    """Drop PATH entries that contain a chromedriver binary (often outdated)."""
    parts = []
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        if not directory:
            continue
        driver_path = os.path.join(directory, "chromedriver")
        if os.path.isfile(driver_path):
            continue
        parts.append(directory)
    return os.pathsep.join(parts)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless browser mode",
    )


@pytest.fixture(scope="session")
def browser_options(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1920,1080")
    return options


@pytest.fixture(scope="function")
def driver(browser_options):
    path_backup = os.environ.get("PATH")
    try:
        # Ignore stale chromedriver in PATH (e.g. /usr/local/bin); use Selenium Manager.
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
