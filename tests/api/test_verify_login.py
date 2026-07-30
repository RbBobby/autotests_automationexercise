"""
API 7–10: /verifyLogin — login verification scenarios.

Uses existing_user fixture (.env credentials) for happy-path tests.
"""

import pytest

from api.models.credentials import UserCredentials
from api.services.auth_service import AuthService
from tests.api.constants import INVALID_EMAIL, INVALID_PASSWORD

pytestmark = pytest.mark.api


class TestVerifyLoginValid:
    """API 7 — POST with valid email and password."""

    def test_verify_login_with_valid_details(
        self, auth_service: AuthService, existing_user: UserCredentials
    ):
        response = auth_service.verify_login(existing_user)
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert body.message == "User exists!"


class TestVerifyLoginMissingEmail:
    """API 8 — POST without email field."""

    def test_verify_login_without_email_returns_400(
        self, auth_service: AuthService, existing_user: UserCredentials
    ):
        response = auth_service.verify_login_missing_email(existing_user.password)
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 400
        assert body.message == (
            "Bad request, email or password parameter is missing in POST request."
        )


class TestVerifyLoginDelete:
    """API 9 — DELETE on verifyLogin endpoint."""

    def test_delete_verify_login_returns_405(self, auth_service: AuthService):
        response = auth_service.delete_verify_login()
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 405
        assert body.message == "This request method is not supported."


class TestVerifyLoginInvalid:
    """API 10 — POST with unknown credentials."""

    def test_verify_login_with_invalid_details_returns_404(self, auth_service: AuthService):
        credentials = UserCredentials(email=INVALID_EMAIL, password=INVALID_PASSWORD)
        response = auth_service.verify_login(credentials)
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 404
        assert body.message == "User not found!"
