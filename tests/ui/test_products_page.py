"""
UI tests for https://automationexercise.com/products (Page Object Model).

Coverage map: TC-01 … TC-15 — see module docstring in test classes below.
Requires Chrome; run with: pytest -m ui -v --headless
"""

import pytest

from tests.ui.constants import EXPECTED_SIDEBAR_BRANDS
from ui.pages.products_page import ProductsPage

pytestmark = pytest.mark.ui


@pytest.fixture(autouse=True)
def products_page(driver) -> ProductsPage:
    """Open /products before each test — every case starts from the same page."""
    page = ProductsPage(driver)
    page.open_products_page()
    return page


class TestPageLoad:
    """TC-01 — URL and document title."""

    def test_url_contains_products(self, products_page: ProductsPage):
        assert "products" in products_page.get_current_url()

    def test_page_title(self, products_page: ProductsPage):
        assert "Automation Exercise" in products_page.get_title()


class TestHeading:
    """TC-02 — main 'All Products' heading."""

    def test_all_products_heading_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.ALL_PRODUCTS_HEADING)

    def test_all_products_heading_text(self, products_page: ProductsPage):
        text = products_page.get_text(ProductsPage.ALL_PRODUCTS_HEADING)
        assert "ALL PRODUCTS" in text.upper()


class TestSearchBar:
    """TC-03 — search input and submit button."""

    def test_search_input_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.SEARCH_INPUT)

    def test_search_button_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.SEARCH_BUTTON)


class TestProductList:
    """TC-04 / TC-05 / TC-06 — product grid content."""

    def test_product_list_not_empty(self, products_page: ProductsPage):
        assert products_page.get_product_count() > 0

    def test_all_products_have_names(self, products_page: ProductsPage):
        for name in products_page.get_all_product_names():
            assert name.strip() != "", f"Empty product name: {name!r}"

    def test_all_products_have_prices(self, products_page: ProductsPage):
        for price in products_page.get_all_product_prices():
            assert price.strip() != "", f"Empty price: {price!r}"

    def test_prices_contain_currency_symbol(self, products_page: ProductsPage):
        for price in products_page.get_all_product_prices():
            assert "Rs." in price, f"Price missing currency: {price!r}"

    def test_product_images_present(self, products_page: ProductsPage):
        for img in products_page.find_elements(ProductsPage.PRODUCT_IMAGES):
            src = img.get_attribute("src")
            assert src and src.strip(), "Product image with empty src"


class TestViewProductLinks:
    """TC-07 — 'View Product' link per card."""

    def test_view_product_links_present(self, products_page: ProductsPage):
        assert len(products_page.find_elements(ProductsPage.VIEW_PRODUCT_LINKS)) > 0

    def test_view_product_links_count_matches_cards(self, products_page: ProductsPage):
        card_count = products_page.get_product_count()
        link_count = len(products_page.find_elements(ProductsPage.VIEW_PRODUCT_LINKS))
        assert link_count == card_count


class TestSearch:
    """TC-08 / TC-09 — client-side product search."""

    def test_search_returns_relevant_results(self, products_page: ProductsPage):
        query = "Top"
        products_page.search_for_product(query)
        results = products_page.get_search_results()
        assert len(results) > 0
        assert any(query.lower() in name.lower() for name in results)

    def test_search_input_updates_product_list(self, products_page: ProductsPage):
        original_count = products_page.get_product_count()
        products_page.search_for_product("Jeans")
        assert products_page.get_product_count() <= original_count

    def test_search_with_no_match_shows_empty_list(self, products_page: ProductsPage):
        products_page.search_for_product("xyznonexistentproduct123")
        assert len(products_page.get_search_results()) == 0


class TestAddToCart:
    """TC-10 / TC-11 — cart modal after Add to cart."""

    def test_add_to_cart_opens_modal(self, products_page: ProductsPage):
        products_page.hover_and_add_to_cart(index=0)
        assert products_page.is_element_visible(ProductsPage.CART_MODAL)

    def test_cart_modal_can_be_dismissed(self, products_page: ProductsPage):
        products_page.hover_and_add_to_cart(index=0)
        products_page.dismiss_cart_modal()
        assert not products_page.is_element_visible(ProductsPage.CART_MODAL)


class TestCategorySidebar:
    """TC-12 / TC-13 — left sidebar categories."""

    def test_left_sidebar_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.LEFT_SIDEBAR)

    def test_category_section_heading_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_SECTION)

    def test_category_women_link_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_WOMEN)

    def test_category_men_link_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_MEN)

    def test_category_kids_link_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_KIDS)


class TestBrandsSidebar:
    """TC-14 — brands block in sidebar (UI text is uppercase)."""

    def test_brands_section_heading_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.BRANDS_SECTION)

    def test_brand_links_not_empty(self, products_page: ProductsPage):
        assert len(products_page.get_brand_names()) > 0

    @pytest.mark.parametrize("brand", EXPECTED_SIDEBAR_BRANDS)
    def test_expected_brand_present(self, products_page: ProductsPage, brand: str):
        brands_upper = [b.upper() for b in products_page.get_brand_names()]
        assert any(brand in b for b in brands_upper)


class TestNavigation:
    """TC-15 — navbar and product details navigation."""

    def test_view_product_navigates_to_details(self, products_page: ProductsPage):
        products_page.click_view_product(index=0)
        assert "product_details" in products_page.get_current_url()

    def test_navbar_home_link_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.NAV_HOME)

    def test_navbar_cart_link_visible(self, products_page: ProductsPage):
        assert products_page.is_element_visible(ProductsPage.NAV_CART)
