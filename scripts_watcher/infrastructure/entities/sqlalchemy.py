import uuid
from datetime import datetime
from typing import Optional, Literal

from sqlalchemy import ForeignKey, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(),
                                                 onupdate=func.current_timestamp())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, index=True, server_default=None)

    def soft_delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None


class Campaign(BaseEntity):
    __tablename__ = 'campaigns'

    name: Mapped[str]
    welcome_message: Mapped[str]
    chats: Mapped[list[str]] = mapped_column(JSONB)
    plus_keywords: Mapped[list[str]] = mapped_column(JSONB)
    minus_keywords: Mapped[list[str]] = mapped_column(JSONB)
    gpt_settings_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('gpt_settings.id'))
    scope: Mapped[str]
    new_lead_wait_interval_seconds: Mapped[str] = mapped_column(server_default='180-300')
    chat_answer_wait_interval_seconds: Mapped[str] = mapped_column(server_default='15-30')

    enabled: Mapped[Optional[bool]]
    type: Mapped[Optional[Literal["Native integration", "Monitoring"]]]
