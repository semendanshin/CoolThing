from dataclasses import dataclass

from pydantic import BaseModel


class BotCreateBase(BaseModel):
    app_id: int
    app_hash: str
    phone: str


class BotConnect(BotCreateBase):
    auth_code: str


class BotConnect2FA(BotCreateBase):
    password: str
