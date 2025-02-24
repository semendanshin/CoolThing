import uuid
from datetime import datetime
from typing import Literal, Optional

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    bot_index: int
    text: str

    model_config = ConfigDict(from_attributes=True)


class Script(Document):
    id: uuid.UUID
    name: str
    type: Literal["Native integration", "Monitoring"]
    messages: list[Message]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = 'scripts'


class ScriptForCampaign(Document):
    id: uuid.UUID
    script_id: uuid.UUID
    campaign_id: uuid.UUID
    bots_mapping: dict[str, str]
    created_at: datetime
    updated_at: datetime

    done: bool
    stopped: bool

    class Settings:
        name = 'scripts_for_campaigns'


class MessageProcess(BaseModel):
    text: str
    bot_id: uuid.UUID

    sent_at: Optional[datetime] = Field(default=None)
    will_be_sent: bool = Field(default=True)


class ChatProcess(BaseModel):
    chat_link: str
    messages: list[MessageProcess]

    processed_at: Optional[datetime] = Field(default=None)
    is_successful: bool = Field(default=False)


class ActiveScriptProcess(Document):
    id: uuid.UUID
    sfc_id: uuid.UUID
    target_chats: list[str]
    process: list[ChatProcess]

    processed_at: Optional[datetime] = Field(default=None)
    is_successful: Optional[bool] = Field(default=False)
    is_failed: bool = Field(default=False)

    class Settings:
        name = 'active_scripts_process'
