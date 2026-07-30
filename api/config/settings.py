"""
Environment-based configuration for API tests.

Values come from .env (via python-dotenv) or OS environment variables.
Copy .env.example → .env and set TEST_USER_* for login tests (API 7–8).
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_BASE_URL = "https://automationexercise.com/api"
DEFAULT_API_TIMEOUT = 30


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings for the API test suite."""

    api_base_url: str
    api_timeout: int
    test_user_email: str
    test_user_password: str


def get_settings() -> Settings:
    """Build Settings from environment; empty credentials → login tests skipped."""
    return Settings(
        api_base_url=os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/"),
        api_timeout=int(os.getenv("API_TIMEOUT", DEFAULT_API_TIMEOUT)),
        test_user_email=os.getenv("TEST_USER_EMAIL", ""),
        test_user_password=os.getenv("TEST_USER_PASSWORD", ""),
    )
