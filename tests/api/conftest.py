import pytest

from api.client.api_client import ApiClient
from api.config.settings import Settings, get_settings
from api.models.user_factory import UserFactory
from api.services.auth_service import AuthService
from api.services.brands_service import BrandsService
from api.services.products_service import ProductsService
from api.services.search_service import SearchService
from api.services.user_service import UserService


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> ApiClient:
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
def valid_user_payload() -> dict:
    return UserFactory.build_user_payload()


@pytest.fixture(scope="session")
def existing_user(settings: Settings) -> dict:
    if not settings.test_user_email or not settings.test_user_password:
        pytest.skip(
            "TEST_USER_EMAIL and TEST_USER_PASSWORD must be set in .env for login tests"
        )
    return {
        "email": settings.test_user_email,
        "password": settings.test_user_password,
    }


@pytest.fixture
def registered_user(user_service: UserService, valid_user_payload: dict) -> dict:
    create_response = user_service.create_account(valid_user_payload)
    body = create_response.json
    assert body["responseCode"] == 201, (
        f"User creation failed: {body.get('message', body)}"
    )
    yield valid_user_payload
    delete_response = user_service.delete_account(
        email=valid_user_payload["email"],
        password=valid_user_payload["password"],
    )
    assert delete_response.json["responseCode"] == 200
