from fastapi import Form

from domain.bots import BotCreate


def bot_create_form(
        api_hash: str = Form(...),
        api_id: int = Form(...),
        proxy: str = Form(...),
) -> BotCreate:
    return BotCreate(
        api_hash=api_hash,
        api_id=api_id,
        proxy=proxy,
    )
