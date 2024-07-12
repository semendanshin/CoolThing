from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(kw_only=True)
class BotOverview:
    nickname: str
    scope: str
    messages_count: int
    chats_ratio: str
    proxy: str
    proxy_status: bool
    unread_messages: int


class BotCreate(BaseModel):
    api_hash: str
    api_id: int
    proxy: str


class BotConnect(BaseModel):
    auth_code: str


class BotConnect2FA(BaseModel):
    password: str
