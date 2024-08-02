import uuid

from sqlalchemy import select, text, update

from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from domain.dto.chat import ChatCreateDTO, ChatUpdateDTO
from domain.models import Chat as ChatModel
from domain.schemas.chats import ChatInfo, Chat as ChatDTO, Message
from infrastructure.entities import Chat
from infrastructure.repositories import AbstractSQLAlchemyRepository


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

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[ChatInfo]:
        statement = text(
            """
            SELECT
                c.id as id,
                w.username as bot_nickname,
                c.username as user_nickname,
                c.lead_chat_id as user_id,
                m.text as last_message,
                c.auto_reply as auto_reply
            FROM chats c
            JOIN (select chat_id, text from messages order by created_at desc limit 1) m on m.chat_id = c.id
            JOIN public.workers w on w.id = c.worker_id
            JOIN public.campaigns c2 on c2.id = c.campaign_id
            LIMIT :limit OFFSET :offset
            """
        ).bindparams(limit=limit, offset=offset)

        async with self.session_maker() as session:
            result = await session.execute(statement)
            rows = result.fetchall()
        return [
            ChatInfo(
                id=str(row.id),
                bot_nickname=row.bot_nickname,
                user_nickname=row.user_nickname,
                user_id=row.user_id,
                last_message=row.last_message,
                status="online",
                auto_reply=row.auto_reply,
            )
            for row in rows
        ]

    async def get_dto(self, obj_id: str) -> ChatDTO:
        uuid_obj_id = uuid.UUID(obj_id)

        chat_statement = text(
            """
            SELECT
                c.id as id,
                w.username as bot_nickname,
                c.username as user_nickname,
                c.lead_chat_id as user_id,
                m.text as last_message,
                c.auto_reply as auto_reply
            FROM chats c
            JOIN (select chat_id, text from messages order by created_at desc limit 1) m on m.chat_id = c.id
            JOIN public.workers w on w.id = c.worker_id
            WHERE c.id = :id
            """
        ).bindparams(id=uuid_obj_id)

        messages_statement = text(
            """
            SELECT
                m.text as text,
                m.created_at as sent_at,
                m.is_outgoing as type
            FROM messages m
            WHERE m.chat_id = :id
            ORDER BY m.created_at
            """
        ).bindparams(id=uuid_obj_id)

        async with self.session_maker() as session:
            chat_result = await session.execute(chat_statement)
            chat_row = chat_result.fetchone()
            messages_result = await session.execute(messages_statement)
            messages_rows = messages_result.fetchall()

        messages = [
            Message(
                text=row.text,
                sent_at=row.sent_at,
                type="outcome" if row.type else "income",
            )
            for row in messages_rows
        ]

        chat_info = ChatDTO(
            info=ChatInfo(
                id=str(chat_row.id),
                bot_nickname=chat_row.bot_nickname,
                user_nickname=chat_row.user_nickname,
                user_id=chat_row.user_id,
                last_message=chat_row.last_message,
                status="online",
                auto_reply=chat_row.auto_reply,
            ),
            messages=messages,
        )

        return chat_info

    async def set_auto_reply(self, chat_id: str, auto_reply: bool) -> None:
        uuid_chat_id = uuid.UUID(chat_id)
        statement = update(Chat).where(Chat.id == uuid_chat_id).values(auto_reply=auto_reply)
        async with self.session_maker() as session:
            async with session.begin():
                await session.execute(statement)
        return None
