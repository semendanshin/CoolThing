from sqlalchemy import select

from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from domain.dto.chat import ChatCreateDTO, ChatUpdateDTO
from infrastructure.entities import Chat
from infrastructure.repositories import AbstractSQLAlchemyRepository
from domain.models import Chat as ChatModel


class ChatsRepository(
    AbstractSQLAlchemyRepository[
        Chat, ChatModel, ChatCreateDTO, ChatUpdateDTO
    ],
    ChatsRepositoryInterface,
):

    def entity_to_model(self, entity: Chat) -> ChatModel:
        return ChatModel(
            id=entity.id,
            campaign_id=entity.campaign_id,
            telegram_chat_id=entity.telegram_chat_id,
            worker_id=entity.worker_id,
            username=entity.username,
            status=entity.status,
            lead_message=entity.lead_message,
            lead_chat_id=entity.lead_chat_id,
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
        )

    async def get_by_worker_id(self, worker_id: str) -> list[ChatModel]:
        async with self.session_maker() as session:
            entities = (await session.execute(select(Chat).where(Chat.worker_id == worker_id))).scalars().all()
        return [
            self.entity_to_model(entity) for entity in entities
        ]