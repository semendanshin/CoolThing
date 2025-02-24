import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, BigInteger, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

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


class Worker(BaseEntity):
    __tablename__ = 'workers'

    app_id: Mapped[str]
    app_hash: Mapped[str]
    session_string: Mapped[str]
    proxy: Mapped[Optional[str]]
    campaign_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), ForeignKey('campaigns.id'))
    role: Mapped[str] = mapped_column(server_default='parser')
    status: Mapped[str] = mapped_column(server_default='stoped')
    username: Mapped[str]
    bio: Mapped[Optional[str]]


class GPT(BaseEntity):
    __tablename__ = 'gpt_settings'

    name: Mapped[str]
    model: Mapped[str]
    assistant: Mapped[Optional[str]]
    token: Mapped[str]
    service_prompt: Mapped[Optional[str]]
    proxy: Mapped[Optional[str]]


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


class Chat(BaseEntity):
    __tablename__ = 'chats'

    campaign_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), ForeignKey('campaigns.id'))
    worker_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('workers.id'))
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]]
    status: Mapped[Optional[str]]
    lead_message: Mapped[Optional[str]]
    lead_chat_id: Mapped[Optional[str]]
    auto_reply: Mapped[bool] = mapped_column(server_default='true')


class Message(BaseEntity):
    __tablename__ = 'messages'

    chat_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('chats.id'))
    text: Mapped[str]
    is_outgoing: Mapped[bool]


class BotBundles(BaseEntity):
    __tablename__ = 'bots_bundles'

    name: Mapped[str]
    bots: Mapped[list[Worker]] = relationship(
        'Worker',
        secondary='bots_bundles_mappings',
        back_populates='bundles'
    )


class BotBundlesMapping(BaseEntity):
    __tablename__ = 'bots_bundles_mappings'

    bot_id: Mapped[UUID] = mapped_column(ForeignKey('workers.id'))
    bundle_id: Mapped[UUID] = mapped_column(ForeignKey('bots_bundles.id'))
