from dataclasses import dataclass

from abstractions.repositories import UOWInterface
from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from abstractions.repositories.MessagesRepositoryInterface import MessagesRepositoryInterface
from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.usecases.MessagesUseCaseInterface import MessagesUseCaseInterface
from domain.dto.message import MessageCreateDTO


@dataclass
class MessagesUseCase(
    MessagesUseCaseInterface
):
    messages_repository: MessagesRepositoryInterface
    chats_repository: ChatsRepositoryInterface
    workers_repository: WorkersRepositoryInterface
    telegram_messages_repository: TelegramMessagesRepositoryInterface
    uow: UOWInterface

    async def send_and_save_message(self, chat_id: str, text: str) -> None:
        async with await self.uow.attach(
                self.messages_repository,
                self.chats_repository,
                self.workers_repository,
        ):
            chat = await self.chats_repository.get(chat_id)
            worker = await self.workers_repository.get(chat.worker_id)
            message_create_dto = MessageCreateDTO(
                chat_id=chat_id,
                text=text,
                is_outgoing=True,
            )
            await self.messages_repository.create(message_create_dto)
            await self.telegram_messages_repository.send_message(
                app_id=worker.app_id,
                app_hash=worker.app_hash,
                session_string=worker.session_string,
                username=chat.username,
                text=text,
            )

        return None
