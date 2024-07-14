from abc import ABC
from dataclasses import dataclass
from typing import Optional

from abstractions.repositories import CRUDRepositoryInterface
from domain.models import Campaign


@dataclass
class CampaignCreateDTO:
    id: str
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    topic: str


@dataclass
class CampaignUpdateDTO:
    id: str
    welcome_message: Optional[str]
    chats: Optional[list[str]]
    plus_keywords: Optional[list[str]]
    minus_keywords: Optional[list[str]]
    gpt_settings_id: Optional[str]
    topic: Optional[str]


class CampaignRepositoryInterface(
    CRUDRepositoryInterface[Campaign, CampaignCreateDTO, CampaignUpdateDTO], ABC
):
    pass
