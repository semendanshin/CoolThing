from fastapi import Form

from domain.schemas.auth import Credentials


def auth_code_form(
        auth_code: str = Form(...),
) -> Credentials:
    return Credentials(
        auth_code=auth_code,
    )
