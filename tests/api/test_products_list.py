"""
API 1: GET All Products List
API 2: POST To All Products List (unsupported method)
"""

import pytest

from api.services.products_service import ProductsService

pytestmark = pytest.mark.api


class TestGetAllProductsList:
    """API 1 — GET /api/productsList"""

    def test_get_all_products_returns_200(self, products_service: ProductsService):
        # Act
        response = products_service.get_products()

        # Assert
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert len(body.products) > 0
        first = body.products[0]
        assert first.id
        assert first.name
        assert first.price
        assert first.brand
        assert first.category


class TestPostToAllProductsList:
    """API 2 — POST /api/productsList"""

    def test_post_products_returns_405(self, products_service: ProductsService):
        # Act
        response = products_service.post_products()

        # Assert
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 405
        assert body.message == "This request method is not supported."
