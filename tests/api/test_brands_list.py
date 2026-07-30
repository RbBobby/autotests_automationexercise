"""
API 3–4: GET /brandsList and unsupported PUT.

Brand names are asserted against EXPECTED_API_BRANDS from constants.
"""

import pytest

from api.services.brands_service import BrandsService
from tests.api.constants import EXPECTED_API_BRANDS

pytestmark = pytest.mark.api


class TestGetAllBrandsList:
    """API 3 — GET /brandsList."""

    def test_get_all_brands_returns_200(self, brands_service: BrandsService):
        response = brands_service.get_brands()
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert len(body.brands) > 0
        assert body.brands[0].brand

    @pytest.mark.parametrize("expected_brand", EXPECTED_API_BRANDS)
    def test_expected_brands_present(self, brands_service: BrandsService, expected_brand: str):
        response = brands_service.get_brands()
        brand_names = [item.brand for item in response.body.brands]
        assert expected_brand in brand_names


class TestPutToAllBrandsList:
    """API 4 — PUT /brandsList (method not allowed)."""

    def test_put_brands_returns_405(self, brands_service: BrandsService):
        response = brands_service.put_brands()
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 405
        assert body.message == "This request method is not supported."
