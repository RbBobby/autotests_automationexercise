from api.client.api_client import ApiClient, ApiResponse


class BrandsService:
    """API Object for /brandsList (API 3–4)."""

    BRANDS_LIST = "/brandsList"

    def __init__(self, client: ApiClient):
        self._client = client

    def get_brands(self) -> ApiResponse:
        return self._client.get(self.BRANDS_LIST)

    def put_brands(self) -> ApiResponse:
        return self._client.put(self.BRANDS_LIST)
