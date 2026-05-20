from api.client.api_client import ApiClient, ApiResponse


class AuthService:
    """API Object for /verifyLogin (API 7–10)."""

    VERIFY_LOGIN = "/verifyLogin"

    def __init__(self, client: ApiClient):
        self._client = client

    def verify_login(self, email: str, password: str) -> ApiResponse:
        return self._client.post(
            self.VERIFY_LOGIN,
            data={"email": email, "password": password},
        )

    def verify_login_missing_email(self, password: str) -> ApiResponse:
        return self._client.post(
            self.VERIFY_LOGIN,
            data={"password": password},
        )

    def delete_verify_login(self) -> ApiResponse:
        return self._client.delete(self.VERIFY_LOGIN)
