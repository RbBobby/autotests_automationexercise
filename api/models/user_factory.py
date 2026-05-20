import uuid
from typing import Any, Dict

from faker import Faker

faker = Faker()


class UserFactory:
    """Builds valid user registration payloads for API 11–14."""

    @staticmethod
    def build_user_payload(**overrides: Any) -> Dict[str, Any]:
        first_name = faker.first_name()
        last_name = faker.last_name()
        unique_id = uuid.uuid4().hex[:12]
        payload = {
            "name": f"{first_name} {last_name}",
            "email": f"api_test_{unique_id}@example.com",
            "password": faker.password(length=12, special_chars=False),
            "title": "Mr",
            "birth_date": "10",
            "birth_month": "5",
            "birth_year": "1990",
            "firstname": first_name,
            "lastname": last_name,
            "company": faker.company(),
            "address1": faker.street_address()[:50],
            "address2": faker.secondary_address()[:50],
            "country": "United States",
            "zipcode": faker.numerify(text="#####"),
            "state": "California",
            "city": faker.city(),
            "mobile_number": faker.numerify(text="##########"),
        }
        payload.update(overrides)
        return payload
