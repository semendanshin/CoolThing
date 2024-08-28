from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from uuid import uuid4


@dataclass(kw_only=True)
class MessageCreateDTO:
    bot: str
    text: str


@dataclass(kw_only=True)
class ScriptCreateDTO:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    messages: list[MessageCreateDTO]


@dataclass(kw_only=True)
class ScriptUpdateDTO:
    id: str = None
    name: str
    type: str
    messages: list[MessageCreateDTO]


@dataclass(kw_only=True)
class ScriptForCampaignCreateDTO:
    id: Optional[str] = field(default_factory=lambda: str(uuid4()))
    script_id: str
    campaign_id: str
    bots_mapping: dict[str, str]


@dataclass(kw_only=True)
class ScriptForCampaignUpdateDTO:
    id: str = None
    script_id: str
    campaign_id: str
    bots_mapping: dict[str, str]
