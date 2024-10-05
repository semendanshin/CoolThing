import logging
from dataclasses import dataclass

from telethon import TelegramClient as Client
from telethon.sessions import StringSession

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface

logger = logging.getLogger(__name__)


@dataclass
class TelethonTelegramMessagesRepository(
    TelegramMessagesRepositoryInterface,
):
    async def send_message(self, app_id: str, app_hash: str, session_string: str, chat_id: str, text: str, reply_to: int) -> None:
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
        await client.send_message(chat_id, text, reply_to=reply_to)
        await client.disconnect()
