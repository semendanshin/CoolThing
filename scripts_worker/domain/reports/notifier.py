import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger(__name__)


class NotificationType(str, Enum):
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


class Notification(BaseModel):
    id: UUID = Field(default_factory=uuid4, )
    type: NotificationType
    created_by: Service
    created_at: datetime = Field(default_factory=datetime.now)


class BotBannedNotification(Notification):
    type: NotificationType = Field(default=NotificationType.BOT_BANNED)

    worker_id: UUID
    comment: str


class ChatSkippedNotification(Notification):
    type: NotificationType = Field(default=NotificationType.CHAT_SKIPPED)

    chat_id: str
    sfc_id: UUID
    on_message: str
    reason: str


class ScriptCrashNotification(Notification):
    type: NotificationType = Field(default=NotificationType.SCRIPT_CRASHED)

    sfc_id: UUID
    on_chat_id: UUID
    on_message: str
    reason: str


class ServiceCrashedNotification(Notification):
    type: NotificationType = Field(default=NotificationType.SERVICE_CRASHED)

    service: Service
    reason: str


class ScriptStartedNotification(Notification):
    type: NotificationType = Field(default=NotificationType.SCRIPT_STARTED)

    sfc_id: UUID
    chats: list[str | int]


class ScriptFinishedNotification(Notification):
    type: NotificationType = Field(default=NotificationType.SCRIPT_FINISHED)

    sfc_id: UUID
    finished_at: datetime
    problems: list[Optional[UUID]]


NotificationTypes = Union[
    BotBannedNotification,
    ChatSkippedNotification,
    ScriptCrashNotification,
    ServiceCrashedNotification,
    ScriptStartedNotification,
    ScriptFinishedNotification,
]
