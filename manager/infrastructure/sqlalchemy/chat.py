from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select

from abstractions.repositories.chat import ChatRepositoryInterface, ChatUpdateDTO, ChatCreateDTO
from domain.models import Chat as ChatModel
from infrastructure.sqlalchemy.abstract import AbstractSQLAlchemyRepository
from infrastructure.sqlalchemy.entities import Chat


@dataclass
class SQLAlchemyChatsRepository(
    AbstractSQLAlchemyRepository[
        Chat,
        ChatModel,
        ChatCreateDTO,
        ChatUpdateDTO,
    ],
    ChatRepositoryInterface,
):
    async def get_by_telegram_chat_id(self, telegram_chat_id: int) -> Optional[Chat]:
        async with self.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(Chat).where(Chat.deleted_at.is_(None)).filter(Chat.telegram_chat_id == telegram_chat_id))
                return result.scalar_one_or_none()

    async def get_by_worker_id(self, worker_id: str) -> list[Chat]:
        async with self.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(Chat).where(Chat.deleted_at.is_(None)).filter(Chat.worker_id == worker_id))
                return [x for x in result.scalars().all()]

    def entity_to_model(self, entity: Chat) -> ChatModel:
        return ChatModel(
            id=str(entity.id),
            campaign_id=str(entity.campaign_id),
            telegram_chat_id=entity.telegram_chat_id,
            worker_id=str(entity.worker_id),
            username=entity.username,
            status=entity.status,
            lead_message=entity.lead_message,
            lead_chat_id=entity.lead_chat_id,
            auto_reply=entity.auto_reply,
        )

    def model_to_entity(self, model: ChatModel) -> Chat:
        return Chat(
            id=model.id,
            campaign_id=model.campaign_id,
            telegram_chat_id=model.telegram_chat_id,
            worker_id=model.worker_id,
            username=model.username,
            status=model.status,
            lead_message=model.lead_message,
            lead_chat_id=model.lead_chat_id,
            auto_reply=model.auto_reply,
        )
