import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EventType(Enum):
    SCRIPT_CRASHED = 'script-crash'
    SERVICE_CRASHED = 'service-crash'
    CHAT_SKIPPED = 'chat-skip'
    BOT_BANNED = 'ban'
    SCRIPT_STARTED = 'script-started'
    SCRIPT_FINISHED = 'script-finished'


class Service(BaseModel):
    id: UUID
    name: str

    tags: list[Optional[str]] = None


class Event(BaseModel):
    # comes from request
    id: UUID
    type: EventType
    created_by: Service
    created_at: datetime


class BotBannedEvent(Event):
    type: EventType = EventType.BOT_BANNED

    worker_id: UUID
    comment: str


class ChatSkippedEvent(Event):
    type: EventType = EventType.CHAT_SKIPPED

    chat_id: int
    sfc_id: UUID
    on_message: str
    reason: str


class ScriptCrashEvent(Event):
    type: EventType = EventType.SCRIPT_CRASHED

    sfc_id: UUID
    on_chat_id: UUID
    on_message: str
    reason: str


class ServiceCrashedEvent(Event):
    type: EventType = EventType.SERVICE_CRASHED

    service: Service
    reason: str


class ScriptStartedEvent(Event):
    type: EventType = EventType.SCRIPT_STARTED

    sfc_id: UUID
    chats: list[str | int]


class ScriptFinishedEvent(Event):
    type: EventType = EventType.SCRIPT_FINISHED

    sfc_id: UUID
    finished_at: datetime
    problems: list[Optional[UUID]]


EventTypes = Union[
    BotBannedEvent,
    ChatSkippedEvent,
    ScriptCrashEvent,
    ServiceCrashedEvent,
    ScriptStartedEvent,
    ScriptFinishedEvent,
]


def event_factory(data: dict) -> Event:
    event_type = data.get("type")

    match event_type:
        case EventType.BOT_BANNED.value:
            logger.info('ban')
            return BotBannedEvent(**data)
        case EventType.CHAT_SKIPPED.value:
            logger.info('skip')
            return ChatSkippedEvent(**data)
        case EventType.SCRIPT_CRASHED.value:
            logger.info('script crash')
            return ScriptCrashEvent(**data)
        case EventType.SERVICE_CRASHED.value:
            logger.info('service crashed')
            return ServiceCrashedEvent(**data)
        case EventType.SCRIPT_STARTED.value:
            logger.info('script started')
            return ScriptStartedEvent(**data)
        case EventType.SCRIPT_FINISHED.value:
            logger.info('script finished')
            return ScriptFinishedEvent(**data)
        case _:
            logger.warning(f'unknown event type: {data}')
            raise ValueError("Unknown event type")
