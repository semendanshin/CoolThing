import logging
from dataclasses import dataclass
from datetime import datetime

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.usecases.WorkersUseCaseInterface import WorkersUseCaseInterface
from domain.models import Worker

logger = logging.getLogger(__name__)


@dataclass
class WorkersUseCase(WorkersUseCaseInterface):
    workers: WorkersRepositoryInterface
    messenger: TelegramMessagesRepositoryInterface

    async def send_message(self, chat_id: str, bot_id: str, message: str):
        logger.info(bot_id)
        logger.info(chat_id)
        worker = await self.workers.get_by_username(username=bot_id)
        # worker = await self.workers.get(obj_id=worker_id)
        await self.messenger.send_message(
            app_id=worker.app_id,
            app_hash=worker.app_hash,
            session_string=worker.session_string,
            chat_id=chat_id,
            text=message,
        )
        logger.info(f"Message {message} from bot {bot_id} was sent to chat {chat_id}")

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
