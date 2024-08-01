from fastapi import Form

from domain.schemas.bots import BotCreateBase


def bot_create_form(
        app_hash: str = Form(...),
        app_id: int = Form(...),
        proxy: str = Form(...),
        phone: str = Form(...),
) -> BotCreateBase:
    return BotCreateBase(
        app_hash=app_hash,
        app_id=app_id,
        proxy=proxy,
        phone=phone,
    )
