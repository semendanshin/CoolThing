import uuid
from dataclasses import dataclass, field

from abstractions.repositories.chat import ChatRepositoryInterface
from abstractions.repositories.gpt import GPTRepositoryInterface
from abstractions.repositories.message import MessageRepositoryInterface, MessageCreateDTO


@dataclass
class GPTUseCase:
    gpt_repo: GPTRepositoryInterface
    messages_repo: MessageRepositoryInterface
    chats_repo: ChatRepositoryInterface

    async def generate_response(self, chat_id: int, text: str) -> str:
        chat = await self.chats_repo.get_by_telegram_chat_id(chat_id)
        await self.messages_repo.create(
            MessageCreateDTO(
                id=str(uuid.uuid4()),
                chat_id=chat.id,
                text=text,
                is_outgoing=False,
            )
        )
        messages = await self.messages_repo.get_by_chat_id(chat.id)
        response = await self.gpt_repo.generate_response(messages)
        await self.messages_repo.create(
            MessageCreateDTO(
                id=str(uuid.uuid4()),
                chat_id=chat.id,
                text=response,
                is_outgoing=True,
            )
        )
        return response
