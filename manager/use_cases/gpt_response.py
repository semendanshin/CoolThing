import uuid
from dataclasses import dataclass, field

from abstractions.repositories.chat import ChatRepositoryInterface
from abstractions.repositories.gpt import GPTRepositoryInterface
from abstractions.repositories.message import MessageRepositoryInterface, MessageCreateDTO
from domain.models import Chat


@dataclass
class GPTUseCase:
    gpt_repo: GPTRepositoryInterface
    messages_repo: MessageRepositoryInterface
    chats_repo: ChatRepositoryInterface

    async def get_chat_by_telegram_chat_id(self, telegram_chat_id: int) -> Chat:
        return await self.chats_repo.get_by_telegram_chat_id(telegram_chat_id)

    async def save_message(self, chat_id: str, text: str, is_outgoing: bool) -> None:
        await self.messages_repo.create(
            MessageCreateDTO(
                chat_id=chat_id,
                text=text,
                is_outgoing=is_outgoing,
            )
        )

    async def generate_response(self, chat_id: str) -> str:
        messages = await self.messages_repo.get_by_chat_id(chat_id)
        response = await self.gpt_repo.generate_response(messages)
        return response
