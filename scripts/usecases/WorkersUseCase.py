import logging
from dataclasses import dataclass
from datetime import datetime

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.usecases.WorkersUseCaseInterface import WorkersUseCaseInterface
from domain.models import Worker
from infrastructure.repositories.telegram.exceptions import NoSuchWorkerException

logger = logging.getLogger(__name__)


@dataclass
class WorkersUseCase(WorkersUseCaseInterface):
    async def join_chat(self, worker_id: str, chat: str | int):
        try:
            worker = await self.get(worker_id)
        except:
            raise NoSuchWorkerException(f"No worker with id {worker_id}")

        await self.messenger.join_chat(worker, chat)

    async def get_by_username(self, username: str) -> Worker:
        return await self.workers.get_by_username(username)

    workers: WorkersRepositoryInterface
    messenger: TelegramMessagesRepositoryInterface

    async def send_message(self, chat_id: str, bot_id: str, message: str, reply_to: int) -> int:
        logger.info(f'Sending message "{message}" from bot {bot_id} to chat {chat_id} (reply to {reply_to})')
        worker = await self.workers.get_by_username(username=bot_id)
        message_id = await self.messenger.send_message(
            app_id=worker.app_id,
            app_hash=worker.app_hash,
            session_string=worker.session_string,
            chat_id=chat_id,
            text=message,
            reply_to=reply_to,
        )
        logger.info(f"Message {message} from bot {bot_id} was sent to chat {chat_id} (reply to {reply_to})")
        return message_id

    async def get(self, bot_id: str) -> Worker:
        return Worker(
            id=bot_id,
            app_id="app_id",
            app_hash="app_hash",
            session_string="session_string",
            proxy="0.0.0.0",
            campaign_id="peonp4-223fre-32432fe",
            role="Manger",
            status="stopped",
            username="username",
            bio="bio",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
