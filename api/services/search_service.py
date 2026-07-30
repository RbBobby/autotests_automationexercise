"""
Search API (scenarios 5–6 on automationexercise.com/api_list).

  POST /searchProduct — search by search_product form field
  POST without search_product — bad request → responseCode 400
"""

from api.client.api_client import ApiClient, ApiResponse


class SearchService:
    """API Object for /searchProduct (API 5–6)."""

    SEARCH_PRODUCT = "/searchProduct"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def search(self, query: str) -> ApiResponse:
        """API 5 — POST with search_product parameter."""
        return self._client.post(
            self.SEARCH_PRODUCT,
            data={"search_product": query},
        )

    def search_without_param(self) -> ApiResponse:
        """API 6 — POST without required search_product (expect 400 in body)."""
        return self._client.post(self.SEARCH_PRODUCT)
