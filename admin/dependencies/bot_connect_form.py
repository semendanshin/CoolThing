from fastapi import Form

from domain.bots import BotConnect


def bot_connect_form(
        auth_code: str = Form(...),
) -> BotConnect:
    return BotConnect(auth_code=auth_code)
