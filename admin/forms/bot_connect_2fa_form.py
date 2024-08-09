from fastapi import Form, Depends

from domain.schemas.bots import BotConnect2FA, BotCreateBase
from forms.bot_create_form import bot_create_form


def bot_connect_2fa_form(
        bot_base: BotCreateBase = Depends(bot_create_form),
        password: str = Form(...),
) -> BotConnect2FA:
    return BotConnect2FA(
        app_id=bot_base.app_id,
        app_hash=bot_base.app_hash,
        phone=bot_base.phone,
        password=password,
        proxy=bot_base.proxy,
    )
