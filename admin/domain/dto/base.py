from datetime import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class CreateDTO(BaseModel):
    id: UUID = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UpdateDTO(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.now)
