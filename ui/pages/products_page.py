from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage


class ProductsPage(BasePage):
    """
    Page Object for https://automationexercise.com/products

    Page structure:
    ├── Navigation bar  (Home, Products, Cart, Signup/Login, …)
    ├── Left sidebar
    │   ├── CATEGORY  (Women / Men / Kids with sub-categories)
    │   └── BRANDS    (Polo, H&M, Madame, …)
    ├── Main panel
    │   ├── "All Products" heading
    │   ├── Search bar  (input + submit button)
    │   └── Product list  — cards each containing:
    │       ├── Product image
    │       ├── Product name  (p tag inside .productinfo)
    │       ├── Price         (h2 tag inside .productinfo)
    │       ├── "Add to cart" hover button
    │       └── "View Product" link
    └── Footer
        └── Subscription block
    """

    URL = "https://automationexercise.com/products"

    # ── Navigation ────────────────────────────────────────────────────────────
    NAVBAR = (By.CSS_SELECTOR, "div#header nav")
    NAV_HOME = (By.CSS_SELECTOR, "a[href='/']")
    NAV_PRODUCTS = (By.CSS_SELECTOR, "a[href='/products']")
    NAV_CART = (By.CSS_SELECTOR, "a[href='/view_cart']")
    NAV_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")

    # ── Page heading ──────────────────────────────────────────────────────────
    ALL_PRODUCTS_HEADING = (By.CSS_SELECTOR, "div.features_items h2.title.text-center")

    # ── Search ────────────────────────────────────────────────────────────────
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_HEADING = (By.CSS_SELECTOR, "h2.title.text-center")

    # ── Product cards ─────────────────────────────────────────────────────────
    PRODUCT_CARDS = (By.CSS_SELECTOR, "div.single-products")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "div.productinfo p")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "div.productinfo h2")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, "div.single-products img")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "div.productinfo a.add-to-cart")
    VIEW_PRODUCT_LINKS = (By.CSS_SELECTOR, "div.product-image-wrapper a[href*='product_details']")

    # Single first product helpers
    FIRST_PRODUCT_NAME = (By.CSS_SELECTOR, "div.productinfo p:first-of-type")
    FIRST_VIEW_PRODUCT = (
        By.CSS_SELECTOR,
        "div.product-image-wrapper:first-child a[href*='product_details']",
    )

    # ── Cart modal (appears after "Add to cart") ───────────────────────────────
    CART_MODAL = (By.ID, "cartModal")
    CART_MODAL_CONTINUE = (By.CSS_SELECTOR, "button[data-dismiss='modal']")
    CART_MODAL_VIEW_CART = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")

    # ── Left sidebar ──────────────────────────────────────────────────────────
    LEFT_SIDEBAR = (By.CSS_SELECTOR, "div.left-sidebar")
    CATEGORY_SECTION = (By.CSS_SELECTOR, "div.left-sidebar h2")      # "CATEGORY" heading
    CATEGORY_WOMEN = (By.CSS_SELECTOR, "a[href='#Women']")
    CATEGORY_MEN = (By.CSS_SELECTOR, "a[href='#Men']")
    CATEGORY_KIDS = (By.CSS_SELECTOR, "a[href='#Kids']")
    BRANDS_SECTION = (By.CSS_SELECTOR, "div.brands_products h2")     # "BRANDS" heading
    BRAND_LINKS = (By.CSS_SELECTOR, "div.brands-name ul li a")

    # ── Footer / Subscription ─────────────────────────────────────────────────
    SUBSCRIPTION_HEADING = (By.CSS_SELECTOR, "div#susbscribe_email_field h2, h2.title:last-of-type")
    SUBSCRIPTION_INPUT = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")

    # ─────────────────────────────────────────────────────────────────────────
    # Page actions
    # ─────────────────────────────────────────────────────────────────────────

    def open_products_page(self):
        """Navigate to the Products page."""
        self.open(self.URL)

    # ── Search ────────────────────────────────────────────────────────────────

    def search_for_product(self, query: str):
        """Type a query into the search field and submit."""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def get_search_results(self) -> list:
        """Return a list of product name strings from the current product grid."""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    # ── Product list helpers ──────────────────────────────────────────────────

    def get_all_product_names(self) -> list[str]:
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_all_product_prices(self) -> list[str]:
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [el.text for el in elements]

    def get_product_count(self) -> int:
        return len(self.find_elements(self.PRODUCT_CARDS))

    def click_view_product(self, index: int = 0):
        """Click the 'View Product' link for the product at the given index (0-based)."""
        links = self.find_elements(self.VIEW_PRODUCT_LINKS)
        links[index].click()

    def hover_and_add_to_cart(self, index: int = 0):
        """
        Hover over a product card to reveal the overlay, then click 'Add to Cart'.
        Uses JavaScript click to avoid the hover-overlay timing issues.
        """
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        self.driver.execute_script("arguments[0].click();", buttons[index])

    def dismiss_cart_modal(self):
        """Continue shopping — close the cart modal."""
        self.click(self.CART_MODAL_CONTINUE)

    # ── Category sidebar ──────────────────────────────────────────────────────

    def get_brand_names(self) -> list[str]:
        elements = self.find_elements(self.BRAND_LINKS)
        return [el.text.strip() for el in elements]

    def click_brand(self, brand_name: str):
        """Click a brand link by its text."""
        brand_links = self.find_elements(self.BRAND_LINKS)
        for link in brand_links:
            if brand_name.upper() in link.text.upper():
                link.click()
                return
        raise ValueError(f"Brand '{brand_name}' not found in the sidebar.")

    def click_category_women(self):
        self.click(self.CATEGORY_WOMEN)

    def click_category_men(self):
        self.click(self.CATEGORY_MEN)

    def click_category_kids(self):
        self.click(self.CATEGORY_KIDS)
