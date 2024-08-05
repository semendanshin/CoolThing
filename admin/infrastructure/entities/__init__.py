import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, BigInteger, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())


class Worker(BaseEntity):
    __tablename__ = 'workers'

    app_id: Mapped[str] = mapped_column(String, nullable=False)
    app_hash: Mapped[str] = mapped_column(String, nullable=False)
    session_string: Mapped[str] = mapped_column(String, nullable=False)
    proxy: Mapped[str] = mapped_column(String, nullable=True)
    campaign_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False, server_default='parser')
    status: Mapped[str] = mapped_column(String, nullable=False, server_default='stoped')
    username: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(String, nullable=True)


class GPT(BaseEntity):
    __tablename__ = 'gpt_settings'

    model: Mapped[str] = mapped_column(String, nullable=False)
    assistant: Mapped[str] = mapped_column(String, nullable=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    service_prompt: Mapped[str] = mapped_column(String, nullable=True)
    proxy: Mapped[str] = mapped_column(String, nullable=True)


class Campaign(BaseEntity):
    __tablename__ = 'campaigns'

    welcome_message: Mapped[str] = mapped_column(String, nullable=False)
    chats: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    plus_keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    minus_keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    gpt_settings_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('gpt_settings.id'), nullable=False)
    scope: Mapped[str] = mapped_column(String, nullable=False)
    new_lead_wait_interval_seconds: Mapped[str] = mapped_column(String, nullable=False, server_default='180-300')
    chat_answer_wait_interval_seconds: Mapped[str] = mapped_column(String, nullable=False, server_default='15-30')


class Chat(BaseEntity):
    __tablename__ = 'chats'

    campaign_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=False)
    worker_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('workers.id'), nullable=False)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    lead_message: Mapped[str] = mapped_column(String, nullable=False)
    lead_chat_id: Mapped[str] = mapped_column(String, nullable=False)
    auto_reply: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true')


class Message(BaseEntity):
    __tablename__ = 'messages'

    chat_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('chats.id'), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    is_outgoing: Mapped[bool] = mapped_column(Boolean, nullable=False)
