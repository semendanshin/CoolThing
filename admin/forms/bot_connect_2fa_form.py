from fastapi import Form

from domain.schemas.bots import BotConnect2FA


def bot_connect_2fa_form(
        password: str = Form(...),
) -> BotConnect2FA:
    return BotConnect2FA(
        password=password,
    )
