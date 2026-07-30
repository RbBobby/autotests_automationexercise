"""
Registration/update payload for user account endpoints (API 11–14).

Field names match form-data keys expected by automationexercise.com API.
Use .to_dict() when passing to UserService; API expects flat string fields.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.models.credentials import UserCredentials


@dataclass
class UserPayload:
    """Mutable user data — tests may tweak fields before update (API 13)."""

    name: str
    email: str
    password: str
    title: str
    birth_date: str
    birth_month: str
    birth_year: str
    firstname: str
    lastname: str
    company: str
    address1: str
    address2: str
    country: str
    zipcode: str
    state: str
    city: str
    mobile_number: str

    def to_dict(self) -> dict[str, str]:
        """Convert to flat dict for application/x-www-form-urlencoded POST/PUT."""
        return asdict(self)

    def with_updates(self, **overrides: Any) -> "UserPayload":
        """Return a copy with selected fields replaced (factory-style overrides)."""
        data = self.to_dict()
        data.update(overrides)
        return UserPayload(**data)

    def as_credentials(self) -> UserCredentials:
        """Email/password view for delete/login helpers."""
        from api.models.credentials import UserCredentials

        return UserCredentials(email=self.email, password=self.password)
