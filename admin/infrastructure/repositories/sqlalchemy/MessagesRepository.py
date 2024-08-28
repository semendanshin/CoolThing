from dataclasses import dataclass

from abstractions.repositories.MessagesRepositoryInterface import MessagesRepositoryInterface
from domain.dto.message import MessageCreateDTO, MessageUpdateDTO
from domain.models import Message as MessageModel
from infrastructure.entities import Message
from infrastructure.repositories.sqlalchemy import AbstractSQLAlchemyRepository


@dataclass
class MessagesRepository(
    AbstractSQLAlchemyRepository[
        Message, MessageModel, MessageCreateDTO, MessageUpdateDTO,
    ],
    MessagesRepositoryInterface,
):
    def entity_to_model(self, entity: Message) -> MessageModel:
        return MessageModel(
            id=str(entity.id),
            chat_id=str(entity.chat_id),
            text=entity.text,
            is_outgoing=entity.is_outgoing,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def model_to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            chat_id=model.chat_id,
            text=model.text,
            is_outgoing=model.is_outgoing,
        )
