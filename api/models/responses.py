"""
Typed parsers for JSON bodies returned by Automation Exercise API.

The site uses camelCase in JSON (responseCode, products, brands).
ApiBody.from_dict() is the single entry point — used by ApiResponse.body.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Product:
    """One item from productsList or searchProduct response."""

    id: int
    name: str
    price: str
    brand: str
    category: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Product":
        return cls(
            id=data["id"],
            name=data["name"],
            price=data["price"],
            brand=data["brand"],
            category=data["category"],
        )


@dataclass
class Brand:
    """One entry from brandsList response."""

    brand: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Brand":
        return cls(brand=data["brand"])


@dataclass
class UserDetail:
    """
    User record from getUserDetailByEmail (API 14).

    Response uses snake_case with underscores (first_name); request payload uses
    firstname — from_dict accepts both conventions for robustness.
    """

    id: int
    name: str
    email: str
    title: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    zipcode: str
    state: str
    city: str
    birth_day: str = ""
    birth_month: str = ""
    birth_year: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserDetail":
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            title=data.get("title", ""),
            first_name=data.get("first_name", data.get("firstname", "")),
            last_name=data.get("last_name", data.get("lastname", "")),
            company=data.get("company", ""),
            address1=data.get("address1", ""),
            address2=data.get("address2", ""),
            country=data.get("country", ""),
            zipcode=data.get("zipcode", ""),
            state=data.get("state", ""),
            city=data.get("city", ""),
            birth_day=data.get("birth_day", data.get("birth_date", "")),
            birth_month=data.get("birth_month", ""),
            birth_year=data.get("birth_year", ""),
        )


@dataclass
class ApiBody:
    """
    Parsed top-level JSON from any Automation Exercise API response.

    response_code maps JSON field "responseCode" (business result, not HTTP code).
    raw keeps the original dict for fields not modeled here.
    """

    response_code: int
    message: Optional[str] = None
    products: list[Product] = field(default_factory=list)
    brands: list[Brand] = field(default_factory=list)
    user: Optional[UserDetail] = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ApiBody":
        products = [Product.from_dict(item) for item in data.get("products", [])]
        brands = [Brand.from_dict(item) for item in data.get("brands", [])]
        user_data = data.get("user")
        user = UserDetail.from_dict(user_data) if user_data else None
        return cls(
            response_code=data["responseCode"],
            message=data.get("message"),
            products=products,
            brands=brands,
            user=user,
            raw=data,
        )
