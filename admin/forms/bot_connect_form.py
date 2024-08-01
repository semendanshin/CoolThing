from fastapi import Form, Depends

from domain.schemas.bots import BotConnect, BotCreateBase
from forms.bot_create_form import bot_create_form


def bot_connect_form(
        bot_base: BotCreateBase = Depends(bot_create_form),
        auth_code: str = Form(...),
) -> BotConnect:
    return BotConnect(
        app_id=bot_base.app_id,
        app_hash=bot_base.app_hash,
        phone=bot_base.phone,
        auth_code=auth_code,
    )
