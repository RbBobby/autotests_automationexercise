import logging
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)


class ApiResponse:
    """Thin wrapper around requests.Response for assertions in tests."""

    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def headers(self) -> dict:
        return dict(self._response.headers)

    @property
    def json(self) -> Any:
        return self._response.json()

    @property
    def ok(self) -> bool:
        return self._response.ok


class ApiClient:
    """HTTP transport layer: session, base URL, timeouts, logging."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def close(self) -> None:
        self._session.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> ApiResponse:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        response = self._session.request(method, url, data=data, params=params, **kwargs)
        logger.debug("%s %s -> %s", method.upper(), url, response.status_code)
        return ApiResponse(response)

    def get(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("DELETE", path, **kwargs)
