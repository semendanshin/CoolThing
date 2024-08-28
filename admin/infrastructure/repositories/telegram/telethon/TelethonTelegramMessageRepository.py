import logging
from dataclasses import dataclass

from telethon import TelegramClient as Client

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface

logger = logging.getLogger(__name__)


@dataclass
class TelethonTelegramMessagesRepository(
    TelegramMessagesRepositoryInterface,
):
    async def send_message(self, app_id: str, app_hash: str, session_string: str, username: str, text: str) -> None:
        if not app_id or not app_hash or not session_string:
            raise ValueError("app_id, app_hash and session_string are required")

        client = Client(
            session=session_string,
            api_id=int(app_id),
            api_hash=app_hash,
            base_logger=logger,
        )
        await client.connect()
        await client.send_message(username, text)
        await client.disconnect()
