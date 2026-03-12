"""
Basic UI tests for https://automationexercise.com/products

Test coverage:
  TC-01  Page URL and title
  TC-02  "All Products" heading is visible
  TC-03  Search bar and button are visible
  TC-04  Product list is not empty
  TC-05  Every product card has a name, price and image
  TC-06  Product prices contain the "Rs." currency symbol
  TC-07  "View Product" links present for every card
  TC-08  Search returns matching results
  TC-09  Search with no match shows empty grid (or appropriate state)
  TC-10  "Add to cart" opens the cart modal
  TC-11  Cart modal can be dismissed (Continue Shopping)
  TC-12  Left sidebar is present
  TC-13  Category section (Women / Men / Kids) is visible
  TC-14  Brands section is visible with expected brands
  TC-15  Clicking "View Product" navigates to the product details page
"""

import pytest

from ui.pages.products_page import ProductsPage

EXPECTED_BRANDS = ["POLO", "H&M", "MADAME", "MAST & HARBOUR", "BABYHUG", "BIBA"]


@pytest.fixture(autouse=True)
def products_page(driver) -> ProductsPage:
    """Open the Products page before every test and return the page object."""
    page = ProductsPage(driver)
    page.open_products_page()
    return page


# ── TC-01 ─────────────────────────────────────────────────────────────────────
class TestPageLoad:
    def test_url_contains_products(self, products_page):
        assert "products" in products_page.get_current_url()

    def test_page_title(self, products_page):
        assert "Automation Exercise" in products_page.get_title()


# ── TC-02 ─────────────────────────────────────────────────────────────────────
class TestHeading:
    def test_all_products_heading_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.ALL_PRODUCTS_HEADING)

    def test_all_products_heading_text(self, products_page):
        text = products_page.get_text(ProductsPage.ALL_PRODUCTS_HEADING)
        assert "ALL PRODUCTS" in text.upper()


# ── TC-03 ─────────────────────────────────────────────────────────────────────
class TestSearchBar:
    def test_search_input_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.SEARCH_INPUT)

    def test_search_button_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.SEARCH_BUTTON)


# ── TC-04 / TC-05 / TC-06 ─────────────────────────────────────────────────────
class TestProductList:
    def test_product_list_not_empty(self, products_page):
        count = products_page.get_product_count()
        assert count > 0, "Expected at least one product on the page"

    def test_all_products_have_names(self, products_page):
        names = products_page.get_all_product_names()
        assert len(names) > 0
        for name in names:
            assert name.strip() != "", f"Found a product with an empty name: '{name}'"

    def test_all_products_have_prices(self, products_page):
        prices = products_page.get_all_product_prices()
        assert len(prices) > 0
        for price in prices:
            assert price.strip() != "", f"Found a product with an empty price: '{price}'"

    def test_prices_contain_currency_symbol(self, products_page):
        """All prices should start with 'Rs.'"""
        prices = products_page.get_all_product_prices()
        for price in prices:
            assert "Rs." in price, f"Price '{price}' does not contain 'Rs.'"

    def test_product_images_present(self, products_page):
        images = products_page.find_elements(ProductsPage.PRODUCT_IMAGES)
        assert len(images) > 0
        for img in images:
            src = img.get_attribute("src")
            assert src and src.strip() != "", "Found a product image with empty src"


# ── TC-07 ─────────────────────────────────────────────────────────────────────
class TestViewProductLinks:
    def test_view_product_links_present(self, products_page):
        links = products_page.find_elements(ProductsPage.VIEW_PRODUCT_LINKS)
        assert len(links) > 0, "No 'View Product' links found"

    def test_view_product_links_count_matches_cards(self, products_page):
        card_count = products_page.get_product_count()
        link_count = len(products_page.find_elements(ProductsPage.VIEW_PRODUCT_LINKS))
        assert link_count == card_count, (
            f"Number of 'View Product' links ({link_count}) "
            f"does not match product cards ({card_count})"
        )


# ── TC-08 / TC-09 ─────────────────────────────────────────────────────────────
class TestSearch:
    def test_search_returns_relevant_results(self, products_page):
        products_page.search_for_product("Top")
        results = products_page.get_search_results()
        assert len(results) > 0, "Search for 'Top' returned no results"
        for name in results:
            assert "Top" in name or "top" in name.lower(), (
                f"Result '{name}' does not seem to match the search query 'Top'"
            )

    def test_search_input_updates_product_list(self, products_page):
        original_count = products_page.get_product_count()
        products_page.search_for_product("Jeans")
        filtered_count = products_page.get_product_count()
        # Jeans is a subset of all products
        assert filtered_count <= original_count

    def test_search_with_no_match_shows_empty_list(self, products_page):
        products_page.search_for_product("xyznonexistentproduct123")
        results = products_page.get_search_results()
        assert len(results) == 0, (
            "Expected 0 results for a nonsense search query but got some"
        )


# ── TC-10 / TC-11 ─────────────────────────────────────────────────────────────
class TestAddToCart:
    def test_add_to_cart_opens_modal(self, products_page):
        products_page.hover_and_add_to_cart(index=0)
        assert products_page.is_element_visible(ProductsPage.CART_MODAL), (
            "Cart modal did not appear after clicking 'Add to Cart'"
        )

    def test_cart_modal_can_be_dismissed(self, products_page):
        products_page.hover_and_add_to_cart(index=0)
        products_page.dismiss_cart_modal()
        # After dismissal the modal should no longer be visible
        assert not products_page.is_element_visible(ProductsPage.CART_MODAL), (
            "Cart modal is still visible after clicking 'Continue Shopping'"
        )


# ── TC-12 / TC-13 ─────────────────────────────────────────────────────────────
class TestCategorySidebar:
    def test_left_sidebar_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.LEFT_SIDEBAR)

    def test_category_section_heading_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_SECTION)

    def test_category_women_link_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_WOMEN)

    def test_category_men_link_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_MEN)

    def test_category_kids_link_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.CATEGORY_KIDS)


# ── TC-14 ─────────────────────────────────────────────────────────────────────
class TestBrandsSidebar:
    def test_brands_section_heading_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.BRANDS_SECTION)

    def test_brand_links_not_empty(self, products_page):
        brands = products_page.get_brand_names()
        assert len(brands) > 0, "No brand links found in the sidebar"

    @pytest.mark.parametrize("brand", EXPECTED_BRANDS)
    def test_expected_brand_present(self, products_page, brand):
        brands_upper = [b.upper() for b in products_page.get_brand_names()]
        found = any(brand in b for b in brands_upper)
        assert found, f"Brand '{brand}' not found in sidebar. Available: {brands_upper}"


# ── TC-15 ─────────────────────────────────────────────────────────────────────
class TestNavigation:
    def test_view_product_navigates_to_details(self, products_page):
        products_page.click_view_product(index=0)
        current_url = products_page.get_current_url()
        assert "product_details" in current_url, (
            f"Expected URL to contain 'product_details', got: {current_url}"
        )

    def test_navbar_home_link_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.NAV_HOME)

    def test_navbar_cart_link_visible(self, products_page):
        assert products_page.is_element_visible(ProductsPage.NAV_CART)
