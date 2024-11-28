import uuid
from datetime import datetime

from beanie import Document
from pydantic import BaseModel, Field


class Message(BaseModel):
    bot_index: int
    text: str


class Script(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    type: str
    bots_count: int
    messages: list[Message]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'scripts'


class ScriptForCampaign(Document):
    id: uuid.UUID
    script_id: uuid.UUID
    campaign_id: uuid.UUID
    bots_mapping: dict[str, str]

    stopped: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'scripts_for_campaigns'
