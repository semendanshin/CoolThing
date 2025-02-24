from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from uuid import uuid4

from pydantic import BaseModel, Field as pydantic_field

from domain.dto.base import CreateDTO, UpdateDTO


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

    stopped: Optional[bool]


class MessageProcessCreateDTO(BaseModel):
    id: str = pydantic_field(default_factory=lambda: str(uuid4()))
    text: str
    bot_id: str

    sent_at: Optional[datetime] = None
    will_be_sent: bool = True


class ChatProcessCreateDTO(BaseModel):
    chat_link: str
    messages: list[MessageProcessCreateDTO]

    processed_at: Optional[datetime] = None
    is_successful: Optional[bool] = None


class ActiveScriptProcessCreateDTO(CreateDTO):
    sfc_id: str
    target_chats: Optional[list[str]] = None
    process: Optional[list[ChatProcessCreateDTO]] = None

    processed_at: Optional[datetime] = None
    is_successful: Optional[bool] = None


class MessageProcessUpdateDTO(BaseModel):
    sent_at: Optional[datetime]
    will_be_sent: Optional[bool]


class ChatProcessUpdateDTO(BaseModel):
    processed_at: Optional[datetime]
    is_successful: Optional[bool]


class ActiveScriptProcessUpdateDTO(UpdateDTO):
    target_chats: Optional[list[str]]
    process: Optional[list[ChatProcessUpdateDTO]]

    processed_at: Optional[datetime]
    is_successful: Optional[bool]
