from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class BotCreateBase(BaseModel):
    app_id: int
    app_hash: str
    phone: str
    proxy: Optional[str] = None


class BotConnect(BotCreateBase):
    auth_code: str


class BotConnect2FA(BotCreateBase):
    password: str
