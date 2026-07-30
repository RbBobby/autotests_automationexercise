"""
Shared constants for API tests.

INVALID_* — negative login (API 10).
EXPECTED_API_BRANDS — canonical brand names from GET /brandsList (API 3).
"""

INVALID_EMAIL = "nonexistent_user@invalid.test"
INVALID_PASSWORD = "wrong_password_12345"

EXPECTED_API_BRANDS = [
    "Polo",
    "H&M",
    "Madame",
    "Mast & Harbour",
    "Babyhug",
    "Allen Solly Junior",
    "Kookie Kids",
    "Biba",
]
