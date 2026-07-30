"""
Products API (scenarios 1–2 on automationexercise.com/api_list).

  GET  /productsList — list all products
  POST /productsList — unsupported → responseCode 405
"""

from api.client.api_client import ApiClient, ApiResponse


class ProductsService:
    """API Object for /productsList (API 1–2)."""

    PRODUCTS_LIST = "/productsList"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get_products(self) -> ApiResponse:
        """API 1 — fetch full product catalog."""
        return self._client.get(self.PRODUCTS_LIST)

    def post_products(self) -> ApiResponse:
        """API 2 — POST is not allowed on this endpoint (expect 405 in body)."""
        return self._client.post(self.PRODUCTS_LIST)
