from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID


@dataclass
class Model(ABC):
    id: str = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass(kw_only=True)
class Worker(Model):
    app_id: str
    app_hash: str
    session_string: str
    proxy: str

    campaign_id: str
    role: str
    status: str

    username: str
    bio: str


@dataclass(kw_only=True)
class GPT(Model):
    model: str
    assistant: str
    token: str
    service_prompt: str


@dataclass(kw_only=True)
class Campaign(Model):
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    scope: str


@dataclass(kw_only=True)
class Chat(Model):
    id: str
    campaign_id: str
    telegram_chat_id: int
    worker_id: str
    username: str
    status: str
    lead_message: str
    lead_chat_id: str


@dataclass(kw_only=True)
class Message(Model):
    id: str
    chat_id: str
    text: str
    is_outgoing: bool
