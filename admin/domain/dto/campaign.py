import uuid
from dataclasses import dataclass, field
from typing import Optional, Literal


@dataclass(kw_only=True)
class CampaignCreateDTO:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    welcome_message: str = None
    chats: list[str] = None
    plus_keywords: list[str] = None
    minus_keywords: list[str] = None
    gpt_settings_id: str = None
    scope: str
    chat_answer_wait_interval_seconds: Optional[str] = None
    new_lead_wait_interval_seconds: Optional[str] = None

    enabled: Optional[bool]
    type: Optional[Literal["Native integration", "Monitoring"]]


@dataclass(kw_only=True)
class CampaignUpdateDTO:
    id: str
    name: Optional[str] = None
    welcome_message: Optional[str] = None
    chats: Optional[list[str]] = None
    plus_keywords: Optional[list[str]] = None
    minus_keywords: Optional[list[str]] = None
    gpt_settings_id: Optional[str] = None
    scope: Optional[str] = None
    chat_answer_wait_interval_seconds: Optional[str] = None
    new_lead_wait_interval_seconds: Optional[str] = None

    enabled: Optional[bool] = None
    type: Optional[Literal["Native integration", "Monitoring"]] = None
