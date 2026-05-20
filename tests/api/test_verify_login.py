"""
API 7: POST To Verify Login with valid details
API 8: POST To Verify Login without email parameter
API 9: DELETE To Verify Login
API 10: POST To Verify Login with invalid details
"""

import pytest

from api.services.auth_service import AuthService
from tests.api.constants import INVALID_EMAIL, INVALID_PASSWORD

pytestmark = pytest.mark.api


class TestVerifyLoginValid:
    """API 7 — POST /api/verifyLogin with valid credentials"""

    def test_verify_login_with_valid_details(self, auth_service: AuthService, existing_user: dict):
        # Arrange
        email = existing_user["email"]
        password = existing_user["password"]

        # Act
        response = auth_service.verify_login(email, password)

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 200
        assert body["message"] == "User exists!"


class TestVerifyLoginMissingEmail:
    """API 8 — POST /api/verifyLogin without email"""

    def test_verify_login_without_email_returns_400(
        self, auth_service: AuthService, existing_user: dict
    ):
        # Arrange
        password = existing_user["password"]

        # Act
        response = auth_service.verify_login_missing_email(password)

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 400
        assert body["message"] == (
            "Bad request, email or password parameter is missing in POST request."
        )


class TestVerifyLoginDelete:
    """API 9 — DELETE /api/verifyLogin"""

    def test_delete_verify_login_returns_405(self, auth_service: AuthService):
        # Act
        response = auth_service.delete_verify_login()

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 405
        assert body["message"] == "This request method is not supported."


class TestVerifyLoginInvalid:
    """API 10 — POST /api/verifyLogin with invalid credentials"""

    def test_verify_login_with_invalid_details_returns_404(self, auth_service: AuthService):
        # Act
        response = auth_service.verify_login(INVALID_EMAIL, INVALID_PASSWORD)

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 404
        assert body["message"] == "User not found!"
