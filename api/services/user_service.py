"""
User account API (scenarios 11–14 on automationexercise.com/api_list).

  POST   /createAccount         — register new user
  DELETE /deleteAccount         — remove user
  PUT    /updateAccount         — update profile
  GET    /getUserDetailByEmail  — fetch user by email query param
"""

from api.client.api_client import ApiClient, ApiResponse
from api.models.credentials import UserCredentials
from api.models.user import UserPayload


class UserService:
    """API Object for user account endpoints (API 11–14)."""

    CREATE_ACCOUNT = "/createAccount"
    DELETE_ACCOUNT = "/deleteAccount"
    UPDATE_ACCOUNT = "/updateAccount"
    GET_USER_BY_EMAIL = "/getUserDetailByEmail"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create_account(self, payload: UserPayload) -> ApiResponse:
        """API 11 — register user; expect responseCode 201."""
        return self._client.post(self.CREATE_ACCOUNT, data=payload.to_dict())

    def delete_account(self, credentials: UserCredentials) -> ApiResponse:
        """API 12 — delete user by email and password."""
        return self._client.delete(
            self.DELETE_ACCOUNT,
            data={"email": credentials.email, "password": credentials.password},
        )

    def update_account(self, payload: UserPayload) -> ApiResponse:
        """API 13 — update existing user; payload must include email/password."""
        return self._client.put(self.UPDATE_ACCOUNT, data=payload.to_dict())

    def get_user_by_email(self, email: str) -> ApiResponse:
        """API 14 — GET user details; email passed as query parameter."""
        return self._client.get(
            self.GET_USER_BY_EMAIL,
            params={"email": email},
        )
