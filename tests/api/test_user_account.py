"""
API 11: POST To Create/Register User Account
API 12: DELETE METHOD To Delete User Account
API 13: PUT METHOD To Update User Account
API 14: GET user account detail by email
"""

import pytest

from api.services.user_service import UserService

pytestmark = pytest.mark.api


class TestCreateUserAccount:
    """API 11 — POST /api/createAccount"""

    def test_create_user_account_returns_201(
        self, user_service: UserService, valid_user_payload: dict
    ):
        # Act
        response = user_service.create_account(valid_user_payload)

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 201
        assert body["message"] == "User created!"

        # Teardown
        user_service.delete_account(
            email=valid_user_payload["email"],
            password=valid_user_payload["password"],
        )


class TestUpdateUserAccount:
    """API 13 — PUT /api/updateAccount"""

    def test_update_user_account_returns_200(
        self, user_service: UserService, registered_user: dict
    ):
        # Arrange
        registered_user["firstname"] = "UpdatedFirst"
        registered_user["lastname"] = "UpdatedLast"

        # Act
        response = user_service.update_account(registered_user)

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 200
        assert body["message"] == "User updated!"


class TestGetUserDetailByEmail:
    """API 14 — GET /api/getUserDetailByEmail"""

    def test_get_user_detail_by_email_returns_200(
        self, user_service: UserService, registered_user: dict
    ):
        # Arrange
        email = registered_user["email"]

        # Act
        response = user_service.get_user_by_email(email)

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 200
        user = body["user"]
        assert user["email"] == email
        assert user["name"] == registered_user["name"]


class TestDeleteUserAccount:
    """API 12 — DELETE /api/deleteAccount"""

    def test_delete_user_account_returns_200(
        self, user_service: UserService, valid_user_payload: dict
    ):
        # Arrange
        create_response = user_service.create_account(valid_user_payload)
        assert create_response.json["responseCode"] == 201

        # Act
        response = user_service.delete_account(
            email=valid_user_payload["email"],
            password=valid_user_payload["password"],
        )

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 200
        assert body["message"] == "Account deleted!"
