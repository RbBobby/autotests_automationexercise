from api.client.api_client import ApiClient, ApiResponse


class ProductsService:
    """API Object for /productsList (API 1–2)."""

    PRODUCTS_LIST = "/productsList"

    def __init__(self, client: ApiClient):
        self._client = client

    def get_products(self) -> ApiResponse:
        return self._client.get(self.PRODUCTS_LIST)

    def post_products(self) -> ApiResponse:
        return self._client.post(self.PRODUCTS_LIST)
