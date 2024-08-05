from fastapi import Form

from domain.schemas.auth import Credentials


def auth_code_form(
        credentials: Credentials
) -> Credentials:
    return credentials
