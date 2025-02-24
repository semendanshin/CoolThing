from fastapi import Response, Cookie

from domain.schemas.auth import Tokens
from config import settings


def update_tokens_in_cookies(response: Response, tokens: Tokens):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        expires=settings.auth.access_token_lifetime_seconds
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        expires=settings.auth.refresh_token_lifetime_seconds
    )


def get_jwt_from_cookies(
        access_token: str = Cookie(default=""),
        refresh_token: str = Cookie(default=""),
):
    return Tokens(
        access_token=access_token,
        refresh_token=refresh_token
    )
