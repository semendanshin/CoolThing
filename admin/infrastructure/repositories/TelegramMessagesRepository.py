from dataclasses import dataclass

from pyrogram import Client

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface


@dataclass
class PyrogramTelegramMessagesRepository(
    TelegramMessagesRepositoryInterface,
):
    async def send_message(self, app_id: str, app_hash: str, session_string: str, username: str, text: str) -> None:
        client = Client(
            name="bot",
            session_string=session_string,
            api_id=app_id,
            api_hash=app_hash,
            in_memory=True,
        )
        await client.start()
        await client.send_message(username, text)
        await client.stop()
        return None
