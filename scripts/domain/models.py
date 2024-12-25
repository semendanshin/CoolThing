from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal
from uuid import uuid4


@dataclass
class Model(ABC):
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


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
    model: str
    token: str
    proxy: str
    assistant: str
    service_prompt: str


@dataclass(kw_only=True)
class Campaign(Model):
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    scope: str
    chat_answer_wait_interval_seconds: str
    new_lead_wait_interval_seconds: str

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

    done: bool
    stopped: bool


@dataclass(kw_only=True)
class MessageProcess:
    id: str
    text: str
    bot_id: str

    sent_at: Optional[datetime] = None
    will_be_sent: bool = True


@dataclass(kw_only=True)
class ChatProcess:
    chat_link: str
    messages: list[MessageProcess]

    processed_at: Optional[datetime] = None
    is_successful: Optional[bool] = None


@dataclass(kw_only=True)
class ActiveScriptProcess(Model):
    sfc_id: str
    target_chats: list[str]
    process: list[ChatProcess]

    processed_at: Optional[datetime] = None
    is_successful: Optional[bool] = None