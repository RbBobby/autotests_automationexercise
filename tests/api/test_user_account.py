"""
API 11–14: user account lifecycle — create, update, get, delete.

registered_user fixture creates/deletes account automatically.
create/delete tests manage their own data to avoid fixture coupling.
"""

import pytest

from api.models.user import UserPayload
from api.services.user_service import UserService

pytestmark = pytest.mark.api


class TestCreateUserAccount:
    """API 11 — POST /createAccount."""

    def test_create_user_account_returns_201(
        self, user_service: UserService, valid_user_payload: UserPayload
    ):
        response = user_service.create_account(valid_user_payload)
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 201
        assert body.message == "User created!"
        user_service.delete_account(valid_user_payload.as_credentials())


class TestUpdateUserAccount:
    """API 13 — PUT /updateAccount."""

    def test_update_user_account_returns_200(
        self, user_service: UserService, registered_user: UserPayload
    ):
        registered_user.firstname = "UpdatedFirst"
        registered_user.lastname = "UpdatedLast"
        response = user_service.update_account(registered_user)
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert body.message == "User updated!"


class TestGetUserDetailByEmail:
    """API 14 — GET /getUserDetailByEmail."""

    def test_get_user_detail_by_email_returns_200(
        self, user_service: UserService, registered_user: UserPayload
    ):
        response = user_service.get_user_by_email(registered_user.email)
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert body.user is not None
        assert body.user.email == registered_user.email
        assert body.user.name == registered_user.name


class TestDeleteUserAccount:
    """API 12 — DELETE /deleteAccount."""

    def test_delete_user_account_returns_200(
        self, user_service: UserService, valid_user_payload: UserPayload
    ):
        create_response = user_service.create_account(valid_user_payload)
        assert create_response.body.response_code == 201
        response = user_service.delete_account(valid_user_payload.as_credentials())
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert body.message == "Account deleted!"
