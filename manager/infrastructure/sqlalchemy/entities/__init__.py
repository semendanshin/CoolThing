import uuid

from sqlalchemy import String, Boolean, ForeignKey, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[str] = mapped_column(String, nullable=False, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(String, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())


class Worker(BaseEntity):
    __tablename__ = 'workers'

    app_id: Mapped[str] = mapped_column(String, nullable=False)
    app_hash: Mapped[str] = mapped_column(String, nullable=False)
    session_string: Mapped[str] = mapped_column(String, nullable=False)
    proxy: Mapped[str] = mapped_column(String, nullable=True)
    campaign_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)


class GPT(BaseEntity):
    __tablename__ = 'gpt_settings'

    model: Mapped[str] = mapped_column(String, nullable=False)
    assistant: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)


class Campaign(BaseEntity):
    __tablename__ = 'campaigns'

    welcome_message: Mapped[str] = mapped_column(String, nullable=False)
    chats: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    plus_keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    minus_keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    gpt_settings_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('gpt_settings.id'), nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False)


class Chat(BaseEntity):
    __tablename__ = 'chats'

    campaign_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=False)
    worker_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('workers.id'), nullable=False)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    lead_message: Mapped[str] = mapped_column(String, nullable=False)
    lead_chat_id: Mapped[str] = mapped_column(String, nullable=False)


class Message(BaseEntity):
    __tablename__ = 'messages'

    chat_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('chats.id'), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    is_outgoing: Mapped[bool] = mapped_column(Boolean, nullable=False)
