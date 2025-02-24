from dataclasses import dataclass

from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.types import SendMessageTypingAction

from abstractions.helpers.message import TelegramClientWrapper


@dataclass
class TelethonTelegramClientWrapper(TelegramClientWrapper):
    async def get_username_by_chat_id(self, chat_id: int) -> str:
        chat = await self.app.get_entity(chat_id)
        return chat.username

    app: TelegramClient

    async def get_chat_id(self, username: str) -> int:
        chat = await self.app.get_entity(username)
        return chat.id

    async def set_typing_status(
            self,
            chat_id: int,
    ) -> None:
        await self.app(
             functions.messages.SetTypingRequest(
                 peer=chat_id, # noqa
                 action=SendMessageTypingAction()
             )
         )

    async def send_message(
            self,
            chat_id: int,
            text: str,
    ) -> None:
        await self.app.send_message(chat_id, text)
