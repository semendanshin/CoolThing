from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import Field, BaseModel

from domain.dto.base import CreateDTO, UpdateDTO


class MessageCreateDTO(BaseModel):
    bot: str
    text: str


class ScriptCreateDTO(CreateDTO):
    name: str
    type: str
    messages: list[MessageCreateDTO]


class ScriptUpdateDTO(UpdateDTO):
    name: str
    type: str
    messages: list[MessageCreateDTO]


class ScriptForCampaignCreateDTO(CreateDTO):
    script_id: str
    campaign_id: str
    bots_mapping: dict[str, str]
    done: bool = Field


class ScriptForCampaignUpdateDTO(UpdateDTO):
    script_id: str
    campaign_id: str
    bots_mapping: dict[str, str]


class MessageProcessCreateDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
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
