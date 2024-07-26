from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class CampaignCreateDTO:
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    topic: str


@dataclass(kw_only=True)
class CampaignUpdateDTO:
    welcome_message: Optional[str] = None
    chats: Optional[list[str]] = None
    plus_keywords: Optional[list[str]] = None
    minus_keywords: Optional[list[str]] = None
    gpt_settings_id: Optional[str] = None
    topic: Optional[str] = None
    scope: Optional[str] = None
