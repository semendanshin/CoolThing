from typing import Optional

from fastapi import Form

from domain.schemas.bots import BotCreateBase


def bot_create_form(
        app_hash: str = Form(...),
        app_id: int = Form(...),
        phone: str = Form(...),
        proxy: Optional[str] = Form(default=None),
) -> BotCreateBase:
    print(f"got proxy: {proxy}, {type(proxy)}")
    return BotCreateBase(
        app_hash=app_hash,
        app_id=app_id,
        phone=phone,
        proxy=proxy,
    )
