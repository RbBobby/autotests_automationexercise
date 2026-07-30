"""
Synthetic user data for API 11–14 (create / update / get / delete account).

Uses Faker for realistic values and uuid for unique emails so parallel runs
do not collide on automationexercise.com.
"""

import uuid
from typing import Any

from faker import Faker

from api.models.user import UserPayload

faker = Faker()


class UserFactory:
    """Builds valid UserPayload instances for registration and update tests."""

    @staticmethod
    def build_user_payload(**overrides: Any) -> UserPayload:
        """
        Create a full registration payload with optional field overrides.

        Example: UserFactory.build_user_payload(email="custom@example.com")
        """
        first_name = faker.first_name()
        last_name = faker.last_name()
        unique_id = uuid.uuid4().hex[:12]
        payload = UserPayload(
            name=f"{first_name} {last_name}",
            email=f"api_test_{unique_id}@example.com",
            password=faker.password(length=12, special_chars=False),
            title="Mr",
            birth_date="10",
            birth_month="5",
            birth_year="1990",
            firstname=first_name,
            lastname=last_name,
            company=faker.company(),
            address1=faker.street_address()[:50],
            address2=faker.secondary_address()[:50],
            country="United States",
            zipcode=faker.numerify(text="#####"),
            state="California",
            city=faker.city(),
            mobile_number=faker.numerify(text="##########"),
        )
        if overrides:
            return payload.with_updates(**overrides)
        return payload
