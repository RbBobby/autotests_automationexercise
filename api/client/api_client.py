"""
HTTP transport layer for Automation Exercise API.

ApiClient  — sends requests via a shared requests.Session (cookies, connection reuse).
ApiResponse — wraps raw Response; exposes typed ApiBody via .body property.

Site quirk: HTTP status is often 200 even on logical errors; use response.body.response_code.
"""

import logging
from functools import cached_property
from typing import Any, Optional

import requests

from api.models.responses import ApiBody

logger = logging.getLogger(__name__)


class ApiResponse:
    """Thin wrapper around requests.Response for assertions in tests."""

    def __init__(self, response: requests.Response) -> None:
        self._response = response

    @property
    def status_code(self) -> int:
        """HTTP status line (usually 200 on this site)."""
        return self._response.status_code

    @property
    def text(self) -> str:
        """Raw response body as text."""
        return self._response.text

    @property
    def headers(self) -> dict:
        """Response headers as a plain dict."""
        return dict(self._response.headers)

    @property
    def json(self) -> Any:
        """Parsed JSON body (untyped dict/list). Prefer .body for typed access."""
        return self._response.json()

    @cached_property
    def body(self) -> ApiBody:
        """Typed view of JSON: response_code, message, products, brands, user."""
        return ApiBody.from_dict(self.json)

    @property
    def ok(self) -> bool:
        """True if HTTP status is 2xx (requests semantics)."""
        return self._response.ok


class ApiClient:
    """
    Shared HTTP client for all API services.

    One session per test run (see tests/api/conftest.py, scope=session).
    All paths are relative to base_url, e.g. GET /productsList.
    """

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def close(self) -> None:
        """Close underlying TCP connections (called in fixture teardown)."""
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
        """
        Low-level request. Services should call get/post/put/delete instead.

        Keyword-only args after * prevent accidental positional data/params mix-ups.
        **kwargs forwards extra requests options (headers, cookies, etc.).
        """
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
