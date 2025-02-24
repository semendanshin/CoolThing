from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

from domain.models.base import Model


class Message(BaseModel):
    id: str
    chat_id: str
    text: str
    is_outgoing: bool


class ScriptMessage(BaseModel):
    bot_index: int
    text: str


class Script(Model):
    name: str
    type: str
    messages: list[ScriptMessage]


class ScriptForCampaign(Model):
    script_id: str
    campaign_id: str
    bots_mapping: dict[str, str]

    done: bool
    stopped: bool


class MessageProcess(BaseModel):
    id: str
    text: str
    bot_id: str

    sent_at: Optional[datetime] = None
    will_be_sent: bool = True


class ChatProcess(BaseModel):
    chat_link: str
    messages: list[MessageProcess]

    processed_at: Optional[datetime] = None
    is_successful: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class ActiveScriptProcess(Model):
    sfc_id: str
    target_chats: Optional[list[str]]
    process: Optional[list[ChatProcess]]

    processed_at: Optional[datetime] = None
    is_successful: Optional[bool] = None
