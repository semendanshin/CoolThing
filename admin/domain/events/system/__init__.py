from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from dependencies.service import get_service_info


class EventType(Enum):
    SERVICE_CRASHED = 'service-crash'


class Service(BaseModel):
    id: UUID
    name: str

    tags: list[Optional[str]] = None


class BaseSystemEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: EventType
    created_by: Service = Field(default_factory=get_service_info)
    created_at: datetime = Field(default_factory=datetime.now)


class ServiceCrashedEvent(BaseSystemEvent):
    type: EventType = EventType.SERVICE_CRASHED

    service: Service = Field(default_factory=get_service_info)
    reason: str
