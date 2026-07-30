"""
Login verification API (scenarios 7–10 on automationexercise.com/api_list).

  POST   /verifyLogin — check email+password
  POST   /verifyLogin — missing email → 400
  DELETE /verifyLogin — unsupported → 405
  POST   invalid credentials → 404
"""

from api.client.api_client import ApiClient, ApiResponse
from api.models.credentials import UserCredentials


class AuthService:
    """API Object for /verifyLogin (API 7–10)."""

    VERIFY_LOGIN = "/verifyLogin"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def verify_login(self, credentials: UserCredentials) -> ApiResponse:
        """API 7 / 10 — POST email and password as form-data."""
        return self._client.post(
            self.VERIFY_LOGIN,
            data={"email": credentials.email, "password": credentials.password},
        )

    def verify_login_missing_email(self, password: str) -> ApiResponse:
        """API 8 — POST with password only (expect 400 in body)."""
        return self._client.post(
            self.VERIFY_LOGIN,
            data={"password": password},
        )

    def delete_verify_login(self) -> ApiResponse:
        """API 9 — DELETE on login endpoint (expect 405 in body)."""
        return self._client.delete(self.VERIFY_LOGIN)
