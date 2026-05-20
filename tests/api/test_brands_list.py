"""
API 3: GET All Brands List
API 4: PUT To All Brands List (unsupported method)
"""

import pytest

from api.services.brands_service import BrandsService

pytestmark = pytest.mark.api

EXPECTED_BRANDS = [
    "Polo",
    "H&M",
    "Madame",
    "Mast & Harbour",
    "Babyhug",
    "Allen Solly Junior",
    "Kookie Kids",
    "Biba",
]


class TestGetAllBrandsList:
    """API 3 — GET /api/brandsList"""

    def test_get_all_brands_returns_200(self, brands_service: BrandsService):
        # Act
        response = brands_service.get_brands()

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 200
        brands = body["brands"]
        assert len(brands) > 0
        assert "brand" in brands[0]

    @pytest.mark.parametrize("expected_brand", EXPECTED_BRANDS)
    def test_expected_brands_present(self, brands_service: BrandsService, expected_brand: str):
        # Act
        response = brands_service.get_brands()

        # Assert
        brand_names = [b["brand"] for b in response.json["brands"]]
        assert expected_brand in brand_names


class TestPutToAllBrandsList:
    """API 4 — PUT /api/brandsList"""

    def test_put_brands_returns_405(self, brands_service: BrandsService):
        # Act
        response = brands_service.put_brands()

        # Assert
        assert response.status_code == 200
        body = response.json
        assert body["responseCode"] == 405
        assert body["message"] == "This request method is not supported."
