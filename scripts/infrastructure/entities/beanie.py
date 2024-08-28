import uuid
from datetime import datetime
from typing import Literal

from beanie import Document
from pydantic import BaseModel, ConfigDict


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

    class Settings:
        name = 'scripts_for_campaigns'
