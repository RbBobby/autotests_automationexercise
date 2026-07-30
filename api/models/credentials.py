"""Email and password pair for login and account deletion flows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    """
    Immutable credentials for /verifyLogin and /deleteAccount.

    frozen=True prevents accidental mutation during a test run.
    """

    email: str
    password: str
