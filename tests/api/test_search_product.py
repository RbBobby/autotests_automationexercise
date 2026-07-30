"""
API 5: POST To Search Product
API 6: POST To Search Product without search_product parameter
"""

import pytest

from api.services.search_service import SearchService

pytestmark = pytest.mark.api

SEARCH_QUERIES = ["top", "tshirt", "jean"]


class TestSearchProduct:
    """API 5 — POST /api/searchProduct with search_product"""

    @pytest.mark.parametrize("query", SEARCH_QUERIES)
    def test_search_product_returns_results(self, search_service: SearchService, query: str):
        # Act
        response = search_service.search(query)

        # Assert
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 200
        assert len(body.products) > 0


class TestSearchProductMissingParam:
    """API 6 — POST /api/searchProduct without search_product"""

    def test_search_without_param_returns_400(self, search_service: SearchService):
        # Act
        response = search_service.search_without_param()

        # Assert
        assert response.status_code == 200
        body = response.body
        assert body.response_code == 400
        assert body.message == (
            "Bad request, search_product parameter is missing in POST request."
        )
