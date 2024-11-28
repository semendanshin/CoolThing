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
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = 'scripts'


class ScriptForCampaign(Document):
    id: uuid.UUID
    script_id: uuid.UUID
    campaign_id: uuid.UUID
    bots_mapping: dict[str, str]

    # defaults to False on app layer on creating
    done: Optional[bool] = Field(default=False)
    stopped: Optional[bool] = Field(default=True)

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = 'scripts_for_campaigns'
