"""
Pytest fixtures for API tests — dependency injection wiring.

Fixture graph (simplified):

  settings (session)
      └── api_client (session)
              ├── products_service
              ├── brands_service
              ├── search_service
              ├── auth_service
              └── user_service
                      ├── valid_user_payload
                      └── registered_user (create → yield → delete)
"""

import pytest

from api.client.api_client import ApiClient
from api.config.settings import Settings, get_settings
from api.models.credentials import UserCredentials
from api.models.user import UserPayload
from api.models.user_factory import UserFactory
from api.services.auth_service import AuthService
from api.services.brands_service import BrandsService
from api.services.products_service import ProductsService
from api.services.search_service import SearchService
from api.services.user_service import UserService


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Load .env once per pytest session."""
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> ApiClient:
    """Shared HTTP session for all API tests; closed after session ends."""
    client = ApiClient(base_url=settings.api_base_url, timeout=settings.api_timeout)
    yield client
    client.close()


@pytest.fixture
def products_service(api_client: ApiClient) -> ProductsService:
    return ProductsService(api_client)


@pytest.fixture
def brands_service(api_client: ApiClient) -> BrandsService:
    return BrandsService(api_client)


@pytest.fixture
def search_service(api_client: ApiClient) -> SearchService:
    return SearchService(api_client)


@pytest.fixture
def auth_service(api_client: ApiClient) -> AuthService:
    return AuthService(api_client)


@pytest.fixture
def user_service(api_client: ApiClient) -> UserService:
    return UserService(api_client)


@pytest.fixture
def valid_user_payload() -> UserPayload:
    """Fresh random user for tests that manage their own lifecycle."""
    return UserFactory.build_user_payload()


@pytest.fixture(scope="session")
def existing_user(settings: Settings) -> UserCredentials:
    """
    Real account from .env for login tests (API 7–8).

    Skips if TEST_USER_EMAIL / TEST_USER_PASSWORD are not set.
    """
    if not settings.test_user_email or not settings.test_user_password:
        pytest.skip("TEST_USER_EMAIL and TEST_USER_PASSWORD must be set in .env for login tests")
    return UserCredentials(
        email=settings.test_user_email,
        password=settings.test_user_password,
    )


@pytest.fixture
def registered_user(user_service: UserService, valid_user_payload: UserPayload) -> UserPayload:
    """
    User created before test, deleted after (yield teardown).

    Use for update/get tests so each case starts with a known account.
    """
    create_response = user_service.create_account(valid_user_payload)
    body = create_response.body
    assert body.response_code == 201, f"User creation failed: {body.message or body.raw}"
    yield valid_user_payload
    delete_response = user_service.delete_account(valid_user_payload.as_credentials())
    assert delete_response.body.response_code == 200
