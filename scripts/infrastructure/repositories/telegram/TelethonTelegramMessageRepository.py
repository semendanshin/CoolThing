import logging
from dataclasses import dataclass

from telethon import TelegramClient as Client
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface
from domain.models import Worker
from infrastructure.repositories.telegram.exceptions import ChatJoinError

logger = logging.getLogger(__name__)


@dataclass
class TelethonTelegramMessagesRepository(
    TelegramMessagesRepositoryInterface,
):
    async def join_chat(self, worker: Worker, chat: str | int):
        logger.info(f"Joining chat {chat} with bot {worker.username} ({worker.id})")

        client = Client(
            session=StringSession(worker.session_string),
            api_id=int(worker.app_id),
            api_hash=worker.app_hash,
            base_logger=logger,
        )

        await client.connect()
        try:
            entity = await client.get_entity(chat)

            await client(JoinChannelRequest(entity))  # noqa
            await client.disconnect()
        except Exception as e:
            await client.disconnect()
            raise ChatJoinError(
                f"There is an error joining chat {chat} with bot {worker.username} ({worker.id}):"
                f" {type(e).__name__}: {e}"
            )

    async def send_message(self, app_id: str, app_hash: str, session_string: str, chat_id: str, text: str,
                           reply_to: int) -> int:
        if not app_id or not app_hash or not session_string:
            raise ValueError("app_id, app_hash and session_string are required")

        logger.info(session_string)

        client = Client(
            session=StringSession(session_string),
            api_id=int(app_id),
            api_hash=app_hash,
            base_logger=logger,

        )
        await client.connect()
        message = await client.send_message(chat_id, text, reply_to=reply_to)
        await client.disconnect()
        return message.id
