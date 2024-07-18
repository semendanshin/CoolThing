from dataclasses import dataclass

from sqlalchemy import select

from abstractions.repositories.message import MessageCreateDTO, MessageUpdateDTO, MessageRepositoryInterface
from domain.models import Message as MessageModel
from infrastructure.sqlalchemy.abstract import AbstractSQLAlchemyRepository
from infrastructure.sqlalchemy.entities import Message


@dataclass
class SQLAlchemyMessagesRepository(
    AbstractSQLAlchemyRepository[
        Message,
        MessageModel,
        MessageCreateDTO,
        MessageUpdateDTO,
    ],
    MessageRepositoryInterface,
):

    async def get_by_chat_id(self, chat_id: str, limit: int = 10, offset: int = 0) -> list[Message]:
        async with self.session_maker() as session:
            query = select(Message).filter(Message.chat_id == chat_id).limit(limit).offset(offset)
            result = await session.execute(query)
            return [self.entity_to_model(entity) for entity in result.scalars().all()]

    def entity_to_model(self, entity: Message) -> MessageModel:
        return MessageModel(
            id=entity.id,
            chat_id=entity.chat_id,
            text=entity.text,
            is_outgoing=entity.is_outgoing,
        )

    def model_to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            chat_id=model.chat_id,
            text=model.text,
            is_outgoing=model.is_outgoing,
        )
