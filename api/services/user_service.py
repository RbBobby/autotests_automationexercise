from typing import Any, Dict

from api.client.api_client import ApiClient, ApiResponse


class UserService:
    """API Object for user account endpoints (API 11–14)."""

    CREATE_ACCOUNT = "/createAccount"
    DELETE_ACCOUNT = "/deleteAccount"
    UPDATE_ACCOUNT = "/updateAccount"
    GET_USER_BY_EMAIL = "/getUserDetailByEmail"

    def __init__(self, client: ApiClient):
        self._client = client

    def create_account(self, payload: Dict[str, Any]) -> ApiResponse:
        return self._client.post(self.CREATE_ACCOUNT, data=payload)

    def delete_account(self, email: str, password: str) -> ApiResponse:
        return self._client.delete(
            self.DELETE_ACCOUNT,
            data={"email": email, "password": password},
        )

    def update_account(self, payload: Dict[str, Any]) -> ApiResponse:
        return self._client.put(self.UPDATE_ACCOUNT, data=payload)

    def get_user_by_email(self, email: str) -> ApiResponse:
        return self._client.get(
            self.GET_USER_BY_EMAIL,
            params={"email": email},
        )
