"""
Base Page Object — shared Selenium helpers for all UI pages.

Provides explicit waits (WebDriverWait) instead of hard sleeps, except for
open() retries on transient network errors against the live site.
"""

import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Substrings in WebDriverException message that indicate a retry-worthy failure.
_TRANSIENT_NAV_ERRORS = (
    "err_connection",
    "err_internet",
    "err_name_not_resolved",
    "timeout",
    "unknown error",
)


class BasePage:
    """Parent class for page objects; holds driver and default 10s wait."""

    def __init__(self, driver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url: str, retries: int = 3) -> None:
        """Navigate to url; retry on transient network errors (live site flakiness)."""
        last_error = None
        for attempt in range(retries):
            try:
                self.driver.get(url)
                return
            except WebDriverException as exc:
                last_error = exc
                message = str(exc).lower()
                is_transient = any(token in message for token in _TRANSIENT_NAV_ERRORS)
                if attempt < retries - 1 and is_transient:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise
        if last_error:
            raise last_error

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    def wait_for_url_contains(self, fragment: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(lambda d: fragment in d.current_url)

    def wait_for_element_visible(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_elements_visible(self, locator: tuple):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def find_element(self, locator: tuple):
        return self.wait_for_element_visible(locator)

    def find_elements(self, locator: tuple):
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple) -> None:
        self.wait_for_element_clickable(locator).click()

    def type_text(self, locator: tuple, text: str) -> None:
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.wait_for_element_visible(locator).text

    def is_element_visible(self, locator: tuple) -> bool:
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except Exception:
            return False

    def is_element_present(self, locator: tuple) -> bool:
        return len(self.driver.find_elements(*locator)) > 0
