"""
Brands API (scenarios 3–4 on automationexercise.com/api_list).

  GET /brandsList — list all brands
  PUT /brandsList — unsupported → responseCode 405
"""

from api.client.api_client import ApiClient, ApiResponse


class BrandsService:
    """API Object for /brandsList (API 3–4)."""

    BRANDS_LIST = "/brandsList"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get_brands(self) -> ApiResponse:
        """API 3 — fetch brand list."""
        return self._client.get(self.BRANDS_LIST)

    def put_brands(self) -> ApiResponse:
        """API 4 — PUT is not allowed (expect 405 in body)."""
        return self._client.put(self.BRANDS_LIST)
