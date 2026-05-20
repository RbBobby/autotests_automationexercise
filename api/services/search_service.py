from api.client.api_client import ApiClient, ApiResponse


class SearchService:
    """API Object for /searchProduct (API 5–6)."""

    SEARCH_PRODUCT = "/searchProduct"

    def __init__(self, client: ApiClient):
        self._client = client

    def search(self, query: str) -> ApiResponse:
        return self._client.post(
            self.SEARCH_PRODUCT,
            data={"search_product": query},
        )

    def search_without_param(self) -> ApiResponse:
        return self._client.post(self.SEARCH_PRODUCT)
