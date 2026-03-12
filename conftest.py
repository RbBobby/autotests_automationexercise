import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
    options.add_argument("--window-size=1920,1080")
    return options


@pytest.fixture(scope="function")
def driver(browser_options):
    driver = webdriver.Chrome(options=browser_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()
