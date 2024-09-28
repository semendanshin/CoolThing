from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal
from uuid import uuid4, UUID


@dataclass
class Model(ABC):
    id: str = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass(kw_only=True)
class Worker(Model):
    app_id: str
    app_hash: str
    session_string: str
    proxy: Optional[str] = None

    campaign_id: Optional[str] = None
    role: str
    status: str

    username: str
    bio: Optional[str] = None

    chats: Optional[list[str]] = None


@dataclass(kw_only=True)
class GPT(Model):
    name: str
    model: str
    token: str
    proxy: str
    assistant: str
    service_prompt: str


@dataclass(kw_only=True)
class Campaign(Model):
    name: str
    welcome_message: str = None
    chats: list[str] = None
    plus_keywords: list[str] = None
    minus_keywords: list[str] = None
    gpt_settings_id: str = None
    scope: str
    chat_answer_wait_interval_seconds: str
    new_lead_wait_interval_seconds: str = None

    enabled: Optional[bool] = None
    type: Optional[Literal["Native integration", "Monitoring"]] = None


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


@dataclass(kw_only=True)
class ScriptMessage:
    bot_index: int
    text: str


@dataclass(kw_only=True)
class Script(Model):
    name: str
    type: str
    messages: list[ScriptMessage]


@dataclass(kw_only=True)
class ScriptForCampaign(Model):
    script_id: str
    campaign_id: str
    bots_mapping: dict[str, str]

    class Settings:
        name = 'scripts_for_campaigns'


@dataclass(kw_only=True)
class Bundle(Model):
    name: str
    bots: list[Worker]
