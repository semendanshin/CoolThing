from dataclasses import dataclass

from pydantic import BaseModel


class BaseBotOverview(BaseModel):
    nickname: str
    scope: str
    proxy: str
    proxy_status: bool


class ManagerBotOverview(BaseBotOverview):
    unread_messages: int
    messages_count: int
    chats_ratio: str


class ParserBotOverview(BaseBotOverview):
    positive_keywords: list[str]
    negative_keywords: list[str]
    chats: list[str]


class BotCreate(BaseModel):
    api_hash: str
    api_id: int
    proxy: str


class BotConnect(BaseModel):
    auth_code: str


class BotConnect2FA(BaseModel):
    password: str


class BaseBotDetails(BaseModel):
    avatar: str
    nickname: str
    bio: str
    scope: str
    proxy: str


class ManagerBotDetails(BaseBotDetails):
    chats_count: int
    api_key: str
    chatgpt_model: str
    chatgpt_assistant: str


class ParserBotDetails(BaseBotDetails):
    positive_keywords: list[str]
    negative_keywords: list[str]
    chats: list[str]
