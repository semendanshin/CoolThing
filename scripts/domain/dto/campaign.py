import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class CampaignCreateDTO:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    scope: str
    chat_answer_wait_interval_seconds: Optional[str] = None
    new_lead_wait_interval_seconds: Optional[str] = None


@dataclass(kw_only=True)
class CampaignUpdateDTO:
    id: str
    welcome_message: Optional[str] = None
    chats: Optional[list[str]] = None
    plus_keywords: Optional[list[str]] = None
    minus_keywords: Optional[list[str]] = None
    gpt_settings_id: Optional[str] = None
    scope: Optional[str] = None
    chat_answer_wait_interval_seconds: Optional[str] = None
    new_lead_wait_interval_seconds: Optional[str] = None
