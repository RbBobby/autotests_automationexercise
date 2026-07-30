"""
Request/response dataclasses for Automation Exercise API.

Request models (outgoing):
  UserPayload      — form fields for create/update account (API 11–14)
  UserCredentials  — email + password for login/delete (API 7–8, 12)

Response models (incoming, via ApiBody.from_dict):
  Product, Brand, UserDetail, ApiBody
"""

from api.models.credentials import UserCredentials
from api.models.responses import ApiBody, Brand, Product, UserDetail
from api.models.user import UserPayload
from api.models.user_factory import UserFactory

__all__ = [
    "ApiBody",
    "Brand",
    "Product",
    "UserCredentials",
    "UserDetail",
    "UserFactory",
    "UserPayload",
]
